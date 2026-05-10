import os
import requests
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_API_KEY}",
    "Content-Type": "application/json"
}


# ── Contacts ──────────────────────────────────────────────────────────────────

def create_or_update_contact(lead: dict) -> dict:
    """
    Create a new contact or update existing one in HubSpot.

    Args:
        lead: dict with email, firstname, lastname, company, phone (optional)

    Returns:
        HubSpot contact dict with id and properties.
    """
    properties = {
        "email": lead.get("email"),
        "firstname": lead.get("name", "").split()[0] if lead.get("name") else "",
        "lastname": " ".join(lead.get("name", "").split()[1:]) if lead.get("name") else "",
        "company": lead.get("company", ""),
        "phone": lead.get("phone", ""),
        "jobtitle": lead.get("role", "")
    }

    # Try to find existing contact by email
    search_response = requests.post(
        f"{BASE_URL}/crm/v3/objects/contacts/search",
        headers=HEADERS,
        json={
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": lead.get("email")
                }]
            }]
        }
    )

    if search_response.status_code == 200:
        results = search_response.json().get("results", [])
        if results:
            # Update existing
            contact_id = results[0]["id"]
            update_response = requests.patch(
                f"{BASE_URL}/crm/v3/objects/contacts/{contact_id}",
                headers=HEADERS,
                json={"properties": properties}
            )
            update_response.raise_for_status()
            print(f"Updated contact: {lead.get('email')}")
            return update_response.json()

    # Create new
    create_response = requests.post(
        f"{BASE_URL}/crm/v3/objects/contacts",
        headers=HEADERS,
        json={"properties": properties}
    )
    create_response.raise_for_status()
    print(f"Created contact: {lead.get('email')}")
    return create_response.json()


def log_note(contact_id: str, note: str) -> dict:
    """
    Log a note/activity against a HubSpot contact.

    Args:
        contact_id: HubSpot contact ID.
        note: Note text to log.

    Returns:
        Created engagement dict.
    """
    payload = {
        "properties": {
            "hs_note_body": note,
            "hs_timestamp": str(int(__import__("time").time() * 1000))
        },
        "associations": [
            {
                "to": {"id": contact_id},
                "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 202}]
            }
        ]
    }

    response = requests.post(
        f"{BASE_URL}/crm/v3/objects/notes",
        headers=HEADERS,
        json=payload
    )
    response.raise_for_status()
    print(f"Note logged for contact {contact_id}")
    return response.json()


def update_lead_stage(contact_id: str, lifecycle_stage: str) -> dict:
    """
    Update the lifecycle stage of a HubSpot contact.

    Lifecycle stages: subscriber, lead, marketingqualifiedlead,
    salesqualifiedlead, opportunity, customer, evangelist, other

    Args:
        contact_id: HubSpot contact ID.
        lifecycle_stage: Target lifecycle stage string.

    Returns:
        Updated contact dict.
    """
    response = requests.patch(
        f"{BASE_URL}/crm/v3/objects/contacts/{contact_id}",
        headers=HEADERS,
        json={"properties": {"lifecyclestage": lifecycle_stage}}
    )
    response.raise_for_status()
    print(f"Contact {contact_id} stage → {lifecycle_stage}")
    return response.json()


if __name__ == "__main__":
    lead = {
        "name": "Sarah Johnson",
        "email": "sarah@acmelogistics.com",
        "company": "Acme Logistics",
        "role": "Head of Operations",
        "phone": "+61412345678"
    }

    print("=== Create/Update Contact ===")
    contact = create_or_update_contact(lead)
    contact_id = contact.get("id")
    print(f"Contact ID: {contact_id}")

    if contact_id:
        print("\n=== Log Note ===")
        log_note(contact_id, "Lead replied with positive interest. Auto-reply sent. Awaiting follow-up.")

        print("\n=== Update Stage ===")
        update_lead_stage(contact_id, "lead")
