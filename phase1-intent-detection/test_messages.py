import pytest
from router import process_message

LEAD = {
    "name": "Test User",
    "company": "Test Co",
    "rep_name": "Alex",
    "company_context": "B2B SaaS platform for sales teams"
}


# ── Intent classification tests ───────────────────────────────────────────────

def test_meeting_request():
    result = process_message("Can we schedule a call to see a demo?", LEAD)
    assert result["intent"] == "meeting_request"
    assert result["action"] == "schedule_meeting"
    assert result["reply"] is not None
    assert "[CALENDLY_LINK]" in result["reply"]
    assert result["confidence"] >= 0.7


def test_pricing_question():
    result = process_message("How much does your product cost?", LEAD)
    assert result["intent"] == "pricing_question"
    assert result["action"] == "send_info"
    assert result["reply"] is not None


def test_objection():
    result = process_message("This seems too expensive for our current budget.", LEAD)
    assert result["intent"] == "objection"
    assert result["action"] == "handle_objection"
    assert result["reply"] is not None


def test_positive_interest():
    result = process_message("Sounds really interesting, tell me more!", LEAD)
    assert result["intent"] == "positive_interest"
    assert result["action"] == "nurture"
    assert result["reply"] is not None


def test_unsubscribe():
    result = process_message("Please remove me from your mailing list.", LEAD)
    assert result["intent"] == "unsubscribe"
    assert result["action"] == "stop"
    assert result["reply"] is None


def test_out_of_office():
    result = process_message("Thanks for reaching out! I'm out of office until Monday.", LEAD)
    assert result["intent"] == "out_of_office"
    assert result["action"] == "schedule_followup"
    assert result["reply"] is not None


# ── Response structure tests ──────────────────────────────────────────────────

def test_response_has_required_fields():
    result = process_message("Hi, I'd love to learn more.", LEAD)
    assert "intent" in result
    assert "confidence" in result
    assert "sentiment" in result
    assert "urgency" in result
    assert "action" in result
    assert "key_signals" in result


def test_confidence_is_valid_float():
    result = process_message("When can we meet?", LEAD)
    assert isinstance(result["confidence"], float)
    assert 0.0 <= result["confidence"] <= 1.0


def test_sentiment_is_valid():
    result = process_message("I'm very excited about this!", LEAD)
    assert result["sentiment"] in ["positive", "neutral", "negative"]


def test_urgency_is_valid():
    result = process_message("We need this ASAP!", LEAD)
    assert result["urgency"] in ["high", "medium", "low"]


def test_key_signals_is_list():
    result = process_message("Can we jump on a quick call?", LEAD)
    assert isinstance(result["key_signals"], list)


# ── Edge case tests ───────────────────────────────────────────────────────────

def test_empty_context_lead():
    minimal_lead = {}
    result = process_message("Tell me more about your product.", minimal_lead)
    assert result["intent"] is not None
    assert result["reply"] is not None


def test_very_short_message():
    result = process_message("Interested.", LEAD)
    assert result["intent"] is not None


def test_gibberish_falls_back_to_unknown_or_valid_intent():
    result = process_message("Blorp flurp wazzle doo.", LEAD)
    valid_intents = [
        "meeting_request", "pricing_question", "objection",
        "positive_interest", "unsubscribe", "out_of_office", "unknown"
    ]
    assert result["intent"] in valid_intents
