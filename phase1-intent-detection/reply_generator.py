import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

REPLY_SYSTEM_PROMPT = """
You are a helpful, professional B2B sales assistant.
Write a concise, personalized reply to a prospect's message.
Rules:
- Keep it under 120 words
- Match their tone (formal if they're formal, friendly if casual)
- Always include a clear next step or call to action
- Never be pushy or salesy
- Use the lead's name if provided
- Sign off as the sales rep name provided
"""


def generate_reply(
    original_message: str,
    intent: str,
    lead_name: str = "there",
    rep_name: str = "Alex",
    company_context: str = "",
    extra_instructions: str = ""
) -> str:
    """
    Generate a context-aware reply based on detected intent.

    Args:
        original_message: The lead's raw message.
        intent: Detected intent string.
        lead_name: First name of the lead.
        rep_name: Name of the sales rep sending the reply.
        company_context: Brief description of your product/company.
        extra_instructions: Intent-specific instructions for the model.

    Returns:
        A ready-to-send reply string.
    """
    user_prompt = f"""
Original message from {lead_name}: "{original_message}"
Detected intent: {intent}
Company context: {company_context}
{f'Additional instructions: {extra_instructions}' if extra_instructions else ''}

Write an appropriate reply from {rep_name}.
"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=REPLY_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    return response.content[0].text.strip()


if __name__ == "__main__":
    test_cases = [
        {
            "original_message": "Hi, can we schedule a call to discuss pricing?",
            "intent": "meeting_request",
            "lead_name": "James",
            "rep_name": "Alex",
            "company_context": "SaaS platform for logistics teams",
            "extra_instructions": "Include a Calendly link placeholder: [CALENDLY_LINK]"
        },
        {
            "original_message": "This seems too expensive for our current budget.",
            "intent": "objection",
            "lead_name": "Maria",
            "rep_name": "Alex",
            "company_context": "AI-powered HR automation tool",
            "extra_instructions": "Acknowledge concern, mention ROI, keep door open."
        },
        {
            "original_message": "Sounds interesting, tell me more about what you offer.",
            "intent": "positive_interest",
            "lead_name": "Tom",
            "rep_name": "Alex",
            "company_context": "Cybersecurity platform for mid-size businesses",
            "extra_instructions": ""
        },
    ]

    for tc in test_cases:
        reply = generate_reply(**tc)
        print(f"\nLead    : {tc['lead_name']}")
        print(f"Intent  : {tc['intent']}")
        print(f"Reply   :\n{reply}")
        print("-" * 60)
