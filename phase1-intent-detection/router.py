from classifier import classify_intent
from reply_generator import generate_reply

ROUTING_RULES = {
    "meeting_request": {
        "action": "schedule_meeting",
        "extra_instructions": (
            "Suggest booking a 30-min call and include a Calendly link placeholder: [CALENDLY_LINK]"
        )
    },
    "pricing_question": {
        "action": "send_info",
        "extra_instructions": (
            "Briefly acknowledge, share that you'll send a pricing overview, "
            "and invite them to a call for tailored pricing."
        )
    },
    "objection": {
        "action": "handle_objection",
        "extra_instructions": (
            "Acknowledge their concern empathetically, provide a brief reassurance, "
            "and keep the conversation going."
        )
    },
    "positive_interest": {
        "action": "nurture",
        "extra_instructions": (
            "Express enthusiasm, recap value briefly, and propose a logical next step."
        )
    },
    "unsubscribe": {
        "action": "stop",
        "extra_instructions": None
    },
    "out_of_office": {
        "action": "schedule_followup",
        "extra_instructions": (
            "Acknowledge their OOO. Don't ask anything. "
            "Simply say you'll follow up when they're back."
        )
    },
    "unknown": {
        "action": "human_review",
        "extra_instructions": (
            "Write a friendly holding reply saying someone from the team "
            "will get back to them shortly."
        )
    }
}


def process_message(message: str, lead: dict) -> dict:
    """
    Full pipeline: classify → route → generate reply.

    Args:
        message: Incoming message text from the lead.
        lead: Dict containing lead context:
              - name (str)
              - company (str)
              - rep_name (str)
              - company_context (str)

    Returns:
        Dict with intent, confidence, sentiment, urgency, action, reply, key_signals.
    """
    # Step 1: Classify intent
    classification = classify_intent(message, context=lead)
    intent = classification["intent"]
    confidence = classification["confidence"]

    # Step 2: Look up routing rule
    rule = ROUTING_RULES.get(intent, ROUTING_RULES["unknown"])
    action = rule["action"]

    # Step 3: Generate reply (skip for unsubscribe)
    reply = None
    if action != "stop":
        reply = generate_reply(
            original_message=message,
            intent=intent,
            lead_name=lead.get("name", "there"),
            rep_name=lead.get("rep_name", "Alex"),
            company_context=lead.get("company_context", ""),
            extra_instructions=rule["extra_instructions"] or ""
        )

    return {
        "intent": intent,
        "confidence": confidence,
        "sentiment": classification.get("sentiment", "neutral"),
        "urgency": classification.get("urgency", "medium"),
        "action": action,
        "reply": reply,
        "key_signals": classification.get("key_signals", [])
    }


if __name__ == "__main__":
    lead = {
        "name": "Sarah",
        "company": "Acme Logistics",
        "rep_name": "Alex",
        "company_context": "We offer AI-powered route optimization for logistics companies."
    }

    messages = [
        "I'd love to see a demo — when can we chat?",
        "How much does your platform cost?",
        "This seems too expensive for our budget.",
        "Sounds interesting, tell me more.",
        "Please remove me from your list.",
        "Thanks! Out of office until Monday.",
        "Blorp flurp wazzle?",
    ]

    for msg in messages:
        print(f"\nMessage : {msg}")
        result = process_message(msg, lead)
        print(f"Intent  : {result['intent']} ({result['confidence']:.0%} confidence)")
        print(f"Sentiment: {result['sentiment']} | Urgency: {result['urgency']}")
        print(f"Action  : {result['action']}")
        print(f"Signals : {result['key_signals']}")
        if result["reply"]:
            print(f"Reply   :\n{result['reply']}")
        print("-" * 60)
