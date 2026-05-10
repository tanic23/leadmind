import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

INTENT_SYSTEM_PROMPT = """
You are an intent detection engine for a B2B sales platform.
Analyze the incoming message and return ONLY a JSON object with:
{
  "intent": one of ["meeting_request", "pricing_question", "objection", "positive_interest", "unsubscribe", "out_of_office", "unknown"],
  "confidence": float between 0.0 and 1.0,
  "key_signals": [list of up to 3 phrases that led to this classification],
  "sentiment": one of ["positive", "neutral", "negative"],
  "urgency": one of ["high", "medium", "low"]
}
Return ONLY valid JSON. No explanation, no markdown, no code fences.
"""


def classify_intent(message: str, context: dict = None) -> dict:
    """
    Classify the intent of an incoming lead message.

    Args:
        message: The raw incoming message text.
        context: Optional dict with lead name, company, prior interactions.

    Returns:
        dict with intent, confidence, key_signals, sentiment, urgency.
    """
    user_content = f"Message: {message}"
    if context:
        user_content += f"\n\nLead context: {json.dumps(context)}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=INTENT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}]
    )

    raw = response.content[0].text.strip()
    return json.loads(raw)


if __name__ == "__main__":
    test_cases = [
        ("I'd love to see a demo. When are you free next week?", {"lead_name": "Sarah", "company": "Acme Corp"}),
        ("This seems too expensive for us right now.", None),
        ("Please remove me from your mailing list.", None),
        ("Thanks! I'm out of office until Monday.", None),
        ("Sounds interesting, tell me more.", {"lead_name": "James", "company": "TechFlow"}),
    ]

    for msg, ctx in test_cases:
        result = classify_intent(msg, context=ctx)
        print(f"\nMessage : {msg}")
        print(f"Result  : {json.dumps(result, indent=2)}")
        print("-" * 60)
