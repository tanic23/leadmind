import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def send_sms(to_number: str, message: str) -> dict:
    """
    Send an SMS via Twilio.

    Args:
        to_number: Recipient phone number in E.164 format (e.g. +61412345678)
        message: SMS text content (keep under 160 chars for 1 segment)

    Returns:
        dict with sid and status.
    """
    if len(message) > 160:
        print(f"Warning: SMS is {len(message)} chars — will be split into multiple segments.")

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"SMS sent to {to_number} | SID: {msg.sid} | Status: {msg.status}")
        return {"sid": msg.sid, "status": msg.status}
    except Exception as e:
        print(f"Twilio error: {e}")
        return {"sid": None, "status": f"error: {str(e)}"}


if __name__ == "__main__":
    result = send_sms(
        to_number="+61412345678",
        message="Hey Sarah, Alex here from RouteAI. Would a 15-min chat about cutting delivery costs make sense?"
    )
    print(result)
