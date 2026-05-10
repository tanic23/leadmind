import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")


def send_email(to_email: str, subject: str, body: str) -> dict:
    """
    Send an email via SendGrid.

    Args:
        to_email: Recipient email address.
        subject: Email subject line.
        body: Plain text email body.

    Returns:
        dict with status_code and message.
    """
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email} | Status: {response.status_code}")
        return {"status_code": response.status_code, "message": "Email sent successfully"}
    except Exception as e:
        print(f"SendGrid error: {e}")
        return {"status_code": 500, "message": str(e)}


if __name__ == "__main__":
    result = send_email(
        to_email="test@example.com",
        subject="Quick question about your ops workflow",
        body="Hi Sarah,\n\nI noticed Acme Logistics is scaling fast...\n\nBest,\nAlex"
    )
    print(result)
