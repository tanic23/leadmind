import sys
import os

# Allow imports from phase1
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "phase1-intent-detection"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "phase2-outreach"))

from router import process_message
from send_email import send_email
from send_sms import send_sms
from calendly import get_scheduling_link
from crm import create_or_update_contact, log_note, update_lead_stage

"""
pipeline.py

Full end-to-end workflow:
1. Receive an incoming message from a lead
2. Classify intent
3. Generate a reply
4. Send reply via the right channel (email or SMS)
5. Log the interaction in HubSpot
6. Update the lead's lifecycle stage
"""


def run_pipeline(message: str, lead: dict, channel: str = "email") -> dict:
    """
    Process an incoming lead message through the full pipeline.

    Args:
        message: Incoming message from the lead.
        lead: Lead dict with name, email, company, phone, rep_name, company_context.
        channel: 'email' or 'sms'

    Returns:
        Pipeline result dict.
    """
    print(f"\n{'='*60}")
    print(f"Processing message from {lead.get('name')} via {channel}")
    print(f"Message: {message}")
    print(f"{'='*60}\n")

    # ── Step 1: Classify + generate reply ──────────────────────────
    result = process_message(message, lead)

    print(f"Intent    : {result['intent']} ({result['confidence']:.0%})")
    print(f"Sentiment : {result['sentiment']} | Urgency: {result['urgency']}")
    print(f"Action    : {result['action']}")

    # ── Step 2: Inject real Calendly link if needed ─────────────────
    reply = result.get("reply", "")
    if reply and "[CALENDLY_LINK]" in reply:
        real_link = get_scheduling_link()
        reply = reply.replace("[CALENDLY_LINK]", real_link)
        result["reply"] = reply

    # ── Step 3: Send reply (skip if action is stop) ─────────────────
    send_result = None
    if result["action"] != "stop" and reply:
        print(f"\nReply:\n{reply}\n")
        if channel == "email" and lead.get("email"):
            send_result = send_email(
                to_email=lead["email"],
                subject=f"Re: {lead.get('company', 'your enquiry')}",
                body=reply
            )
        elif channel == "sms" and lead.get("phone"):
            send_result = send_sms(
                to_number=lead["phone"],
                message=reply[:160]  # Truncate to 1 SMS segment
            )
    elif result["action"] == "stop":
        print("Action is STOP — no reply sent. Marking as unsubscribed.")

    # ── Step 4: Log to CRM ─────────────────────────────────────────
    crm_contact = None
    if lead.get("email"):
        crm_contact = create_or_update_contact(lead)
        contact_id = crm_contact.get("id")

        if contact_id:
            note = (
                f"Intent: {result['intent']} | "
                f"Confidence: {result['confidence']:.0%} | "
                f"Sentiment: {result['sentiment']} | "
                f"Urgency: {result['urgency']}\n"
                f"Message: {message}\n"
                f"Reply sent via {channel}: {reply or 'N/A (no reply sent)'}"
            )
            log_note(contact_id, note)

            # Update lifecycle stage based on intent
            stage_map = {
                "meeting_request": "salesqualifiedlead",
                "positive_interest": "marketingqualifiedlead",
                "pricing_question": "lead",
                "objection": "lead",
                "unsubscribe": "other",
                "out_of_office": "lead",
                "unknown": "subscriber"
            }
            stage = stage_map.get(result["intent"], "lead")
            update_lead_stage(contact_id, stage)

    return {
        "intent": result["intent"],
        "action": result["action"],
        "reply": reply,
        "send_result": send_result,
        "crm_contact_id": crm_contact.get("id") if crm_contact else None
    }


if __name__ == "__main__":
    lead = {
        "name": "Sarah Johnson",
        "email": "sarah@acmelogistics.com",
        "phone": "+61412345678",
        "company": "Acme Logistics",
        "role": "Head of Operations",
        "rep_name": "Alex",
        "company_context": "RouteAI — AI-powered route optimization that cuts delivery costs by 30%"
    }

    # Simulate an incoming message
    incoming = "Hi! I'd love to see a demo of your platform. When are you free?"

    final = run_pipeline(incoming, lead, channel="email")
    print("\n=== Pipeline Complete ===")
    print(f"Intent          : {final['intent']}")
    print(f"Action          : {final['action']}")
    print(f"CRM Contact ID  : {final['crm_contact_id']}")
    print(f"Send Result     : {final['send_result']}")
