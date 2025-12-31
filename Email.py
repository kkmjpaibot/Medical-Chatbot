# Email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Googlesheet import update_email_sent

# -----------------------------
# Email Configuration
# -----------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ADDRESS = "kkmjpaibot@gmail.com"     # Sender email
EMAIL_PASSWORD = "xtcz rcwz jixf ugnp"      # Gmail App Password

AGENT_WHATSAPP = "https://wa.me/60168357258"

# -----------------------------
# Send Campaign 4 Email
# -----------------------------
def send_campaign4_email(session):
    """
    Sends medical/insurance planning summary email.
    Updates Email_sent timestamp ONLY after successful send.
    """

    recipient = session.get("email", "").strip()
    name = session.get("name", "").strip()

    if not recipient:
        print("❌ No email found in session. Email not sent.")
        return False

    # -----------------------------
    # Build Email
    # -----------------------------
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient
    msg["Subject"] = "Your Medical Coverage Summary"

    body = f"""
Hi {name},

Thank you for using our Medical Coverage Planning Tool.
Here is a summary of your details:

Name              : {session.get('name')}
Date of Birth     : {session.get('dob')}
Age               : {session.get('age')}
Current Coverage  : {session.get('coverage')}
Budget Range      : {session.get('budget')}
Selected Plan     : {session.get('plan')}
Monthly Premium   : RM {session.get('premium')}
Phone             : {session.get('phone')}
Email             : {session.get('email')}

If you would like to speak to an agent or WhatsApp us, click below:
{AGENT_WHATSAPP}

Thank you & have a great day.
"""

    msg.attach(MIMEText(body, "plain"))

    # -----------------------------
    # Send Email
    # -----------------------------
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email successfully sent to {recipient}")

        # -----------------------------
        # Update Google Sheet
        # -----------------------------
        ts = update_email_sent(recipient)
        if ts:
            print(f"✅ Email_sent timestamp updated for {recipient} -> {ts}")
        else:
            print(f"⚠️ Could not update Email_sent timestamp for {recipient}")

        # Return the timestamp (or None) so callers can act on it
        return ts

    except Exception as e:
        print("❌ Email sending failed")
        print(e)
        return False
