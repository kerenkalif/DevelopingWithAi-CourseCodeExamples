# Shared Gmail sender — plain Python, no agno / agent dependency.
# Sends a real email via Gmail (smtp.gmail.com + App Password). Everything
# (recipient AND sender details) is a parameter — the caller passes them in.
# Standalone:  send_gmail("a@b.com", "Hi", "Hello", "me@gmail.com", "Me", passkey)

import smtplib
from email.message import EmailMessage


def send_gmail(
    to: str,
    subject: str,
    body: str,
    sender_email: str,
    sender_name: str,
    sender_passkey: str,
) -> str:
    """Send an email to a recipient via Gmail.

    :param to: Recipient email address.
    :param subject: Subject line of the email.
    :param body: Plain-text body of the email.
    :param sender_email: The sender's Gmail address.
    :param sender_name: Display name shown as the sender.
    :param sender_passkey: Gmail App Password used to authenticate.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
        server.login(sender_email, sender_passkey)
        server.send_message(msg)

    return f"Email sent successfully to {to}."


if __name__ == "__main__":
    import os

    target_email = input("To whom send the email? ")
    print(send_gmail(
        to=target_email,
        subject="Test from emails_tool",
        body="It works!",
        sender_email="keren.kalif@gmail.com",
        sender_name="Keren Kalif - Agent",
        sender_passkey=os.environ["GMAIL_APP_PASSWORD_FOR_STOCK_ANALYZER_AGENT"],
    ))
