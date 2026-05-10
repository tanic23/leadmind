import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

EMAIL_SYSTEM_PROMPT = """
You are an expert B2B sales copywriter.
Write a personalized cold outreach email based on the lead data provided.
Rules:
- Subject line: punchy, under 10 words, no spam triggers
- Body: 3 short paragraphs max (opener, value prop, CTA)
- Total body under 150 words
- Sound human, not templated
- Reference something specific about their company or role
- CTA should be low-friction (a question or a short call offer)
- Sign off with the rep's name and title

Return ONLY a JSON object:
{
  "subject": "...",
  "body": "..."
}
No markdown, no code fences, only valid JSON.
"""

SMS_SYSTEM_PROMPT = """
You are a B2B sales assistant writing a cold outreach SMS.
Rules:
- Under 160 characters (one SMS segment)
- Friendly, natural, human tone
- Include the lead's first name
- End with a simple question or call to action
- No links unless told to include one

Return ONLY the SMS text string. No JSON, no explanation.
"""

FOLLOWUP_SYSTEM_PROMPT = """
You are a B2B sales assistant writing a follow-up message.
The lead has not replied to a previous outreach.
Rules:
- Reference that you reached out before (briefly)
- Don't guilt-trip or be passive-aggressive
- Add a small new piece of value or insight
- Keep it under 100 words
- End with a simple yes/no question

Return ONLY the follow-up message text.
"""


def generate_email(lead: dict, rep: dict) -> dict:
    """
    Generate a personalized cold outreach email.

    Args:
        lead: dict with name, company, role, industry, pain_point (optional)
        rep: dict with name, title, company_context

    Returns:
        dict with 'subject' and 'body'
    """
    prompt = f"""
Lead details:
- Name: {lead.get('name', 'there')}
- Company: {lead.get('company', 'their company')}
- Role: {lead.get('role', 'unknown')}
- Industry: {lead.get('industry', 'unknown')}
- Known pain point: {lead.get('pain_point', 'not specified')}

Rep details:
- Rep name: {rep.get('name', 'Alex')}
- Rep title: {rep.get('title', 'Account Executive')}
- Our product/company: {rep.get('company_context', '')}

Write a personalized cold outreach email.
"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        system=EMAIL_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.content[0].text.strip()
    return json.loads(raw)


def generate_sms(lead: dict, rep: dict) -> str:
    """
    Generate a personalized cold outreach SMS.

    Args:
        lead: dict with name, company, role
        rep: dict with name, company_context

    Returns:
        SMS string under 160 characters
    """
    prompt = f"""
Lead: {lead.get('name', 'there')} at {lead.get('company', 'their company')} ({lead.get('role', '')})
Rep: {rep.get('name', 'Alex')} from {rep.get('company_context', 'our company')}

Write a short cold outreach SMS.
"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        system=SMS_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


def generate_followup(lead: dict, rep: dict, channel: str = "email") -> str:
    """
    Generate a follow-up message for a lead who hasn't replied.

    Args:
        lead: dict with name, company, role
        rep: dict with name, company_context
        channel: 'email' or 'sms'

    Returns:
        Follow-up message string
    """
    prompt = f"""
Lead: {lead.get('name', 'there')} at {lead.get('company', '')} ({lead.get('role', '')})
Rep: {rep.get('name', 'Alex')}
Product context: {rep.get('company_context', '')}
Channel: {channel}

Write a follow-up message for someone who hasn't responded to the first outreach.
"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system=FOLLOWUP_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


if __name__ == "__main__":
    lead = {
        "name": "Sarah",
        "company": "Acme Logistics",
        "role": "Head of Operations",
        "industry": "Logistics & Supply Chain",
        "pain_point": "Manual route planning is eating up hours every week"
    }

    rep = {
        "name": "Alex",
        "title": "Account Executive",
        "company_context": "RouteAI — AI-powered route optimization that cuts delivery costs by 30%"
    }

    print("=== COLD EMAIL ===")
    email = generate_email(lead, rep)
    print(f"Subject : {email['subject']}")
    print(f"Body    :\n{email['body']}")

    print("\n=== COLD SMS ===")
    sms = generate_sms(lead, rep)
    print(f"SMS ({len(sms)} chars): {sms}")

    print("\n=== FOLLOW-UP EMAIL ===")
    followup = generate_followup(lead, rep, channel="email")
    print(followup)
