# Email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from Googlesheet import update_email_sent
import os

# -----------------------------
# Email Configuration
# -----------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ADDRESS = "kkmjpaibot@gmail.com"
EMAIL_PASSWORD = "dkxv qnzk pxcj yvzw"

AGENT_WHATSAPP = "https://wa.me/60168357258"

ATTACHMENT_FILE = "Benefits.pdf"

# -----------------------------
# Send Campaign 4 Email
# -----------------------------
def send_campaign4_email(session):
    """
    Sends a friendly, modern medical planning summary email.
    HTML + plain-text fallback.
    Updates Google Sheet only after successful send.
    """

    recipient = session.get("email", "").strip()
    name = session.get("name", "").strip() or "there"

    if not recipient:
        print("❌ No email found in session. Email not sent.")
        return False

    # -----------------------------
    # Create Email
    # -----------------------------
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient
    msg["Subject"] = "🌿 Your Medical Coverage Summary is Ready"

    # -----------------------------
    # Plain Text Fallback
    # -----------------------------
    text_body = f"""
Hi {name},

Thanks for using our Medical Coverage Planning Tool 😊
We’ve put together a quick summary based on what you shared.

Your Details:
- Name: {session.get('name')}
- Date of Birth: {session.get('dob')}
- Age: {session.get('age')}
- Current Coverage: {session.get('coverage')}
- Budget Range: {session.get('budget')}
- Selected Plan: {session.get('plan')}
- Monthly Premium: RM {session.get('premium')}
- Phone: {session.get('phone')}
- Email: {session.get('email')}

If you’d like help understanding your options or want to take the next step,
our agent is happy to assist you on WhatsApp:

{AGENT_WHATSAPP}

Take care & have a wonderful day 🌸
Legacy Medical Planning Team
"""

    # -----------------------------
    # HTML Email (Modern + Friendly)
    # -----------------------------
    html_body = f"""
    <html>
    <body style="margin:0;padding:0;background:#f1f5f9;
                 font-family:'Segoe UI',Arial,Helvetica,sans-serif;">

        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center" style="padding:40px 15px;">

                    <table width="600" cellpadding="0" cellspacing="0"
                        style="background:#ffffff;border-radius:16px;
                               box-shadow:0 20px 40px rgba(15,23,42,0.12);
                               overflow:hidden;">

                        <!-- Header -->
                        <tr>
                            <td style="background:linear-gradient(135deg,#38bdf8,#0ea5e9);
                                       padding:28px;text-align:center;">
                                <h1 style="margin:0;color:#ffffff;font-size:24px;">
                                    🌿 Medical Coverage Summary
                                </h1>
                                <p style="margin:8px 0 0;color:#e0f2fe;font-size:14px;">
                                    Simple. Clear. Made just for you.
                                </p>
                            </td>
                        </tr>

                        <!-- Greeting -->
                        <tr>
                            <td style="padding:28px;color:#334155;font-size:15px;">
                                Hi <strong>{name}</strong> 👋<br><br>
                                Thanks for taking the time to explore your medical coverage options with us.
                                Here’s a friendly summary of what you shared — no jargon, no pressure 😊
                            </td>
                        </tr>

                        <!-- Summary Card -->
                        <tr>
                            <td style="padding:0 28px 20px;">
                                <table width="100%" cellpadding="12" cellspacing="0"
                                    style="border-collapse:collapse;font-size:14px;
                                           background:#f8fafc;border-radius:12px;">
                                    <tr>
                                        <td><strong>Name</strong></td>
                                        <td>{session.get('name')}</td>
                                    </tr>
                                    <tr style="background:#ffffff;">
                                        <td><strong>Date of Birth</strong></td>
                                        <td>{session.get('dob')}</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Age</strong></td>
                                        <td>{session.get('age')}</td>
                                    </tr>
                                    <tr style="background:#ffffff;">
                                        <td><strong>Current Coverage</strong></td>
                                        <td>{session.get('coverage')}</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Budget Comfort Zone</strong></td>
                                        <td>{session.get('budget')}</td>
                                    </tr>
                                    <tr style="background:#ffffff;">
                                        <td><strong>Recommended Plan</strong></td>
                                        <td>{session.get('plan')}</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Estimated Monthly Premium</strong></td>
                                        <td><strong>RM {session.get('premium')}</strong></td>
                                    </tr>
                                </table>
                            </td>
                        </tr>

                        <!-- CTA -->
                        <tr>
                            <td align="center" style="padding:25px 28px;">
                                <p style="font-size:14px;color:#475569;margin-bottom:18px;">
                                    Have questions or want personal guidance?
                                    Our friendly agent is just one click away 💬
                                </p>
                                <a href="{AGENT_WHATSAPP}"
                                   style="background:#22c55e;color:#ffffff;
                                          text-decoration:none;font-weight:600;
                                          padding:14px 34px;border-radius:999px;
                                          display:inline-block;font-size:15px;">
                                     Chat with an Agent on WhatsApp
                                </a>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="padding:22px;text-align:center;
                                       font-size:12px;color:#94a3b8;">
                                You’re always in control — no obligations, no pressure.<br>
                                <strong>Legacy Medical Planning Team</strong><br>
                                Wishing you good health 🌸
                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>
    </html>
    """

    # Attach versions
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    # -----------------------------
    # Attach PDF File
    # -----------------------------
    if os.path.exists(ATTACHMENT_FILE):
        with open(ATTACHMENT_FILE, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{ATTACHMENT_FILE}"'
        )
        msg.attach(part)
        print("Benefits.pdf attached successfully.")
    else:
        print("Benefits.pdf not found. Email sent without attachment.")

    # -----------------------------
    # Send Email
    # -----------------------------
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email successfully sent to {recipient}")

        ts = update_email_sent(recipient)
        if ts:
            print(f"✅ Email_sent timestamp updated for {recipient} -> {ts}")
        else:
            print(f"⚠️ Could not update Email_sent timestamp for {recipient}")

        return ts

    except Exception as e:
        print("❌ Email sending failed")
        print(e)
        return False
