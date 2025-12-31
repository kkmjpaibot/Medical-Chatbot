# googlesheet.py
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# -----------------------------
# Google Sheets Setup
# -----------------------------
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file(
    "ServiceAccount.json",
    scopes=SCOPE
)

client = gspread.authorize(CREDS)

SPREADSHEET_NAME = "ChatBotData"
WORKSHEET_NAME = "Campaign4"

HEADERS = [
    "Name",
    "Date of Birth",
    "Age",
    "Coverage Status",
    "Budget Range",
    "Plan Coverage",
    "Monthly Premium",
    "Phone",
    "Email",
    "Timestamp",
    "WhatsappLink",     # moved from L to K
    "Email TimeStamp"   # moved from K to L
]

# -----------------------------
# Initialize Sheet
# -----------------------------
def init_sheet():
    """Ensure spreadsheet, worksheet, and headers exist."""
    try:
        sh = client.open(SPREADSHEET_NAME)
    except gspread.SpreadsheetNotFound:
        sh = client.create(SPREADSHEET_NAME)

    try:
        sheet = sh.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        sheet = sh.add_worksheet(
            title=WORKSHEET_NAME,
            rows=1000,
            cols=len(HEADERS)
        )

    all_values = sheet.get_all_values()
    if not all_values:
        sheet.append_row(HEADERS)

    return sheet

# -----------------------------
# Generate WhatsApp Link
# -----------------------------
def generate_whatsapp_link(phone):
    if not phone:
        return ""
    phone_clean = "".join(filter(str.isdigit, str(phone)))
    if phone_clean.startswith("0"):
        phone_clean = "6" + phone_clean
    return f"https://wa.me/{phone_clean}"

# -----------------------------
# Append new session
# -----------------------------
def save_session_after_email(session_data, email_sent=False):
    """
    Append a new row for Campaign 4
    """
    sheet = init_sheet()

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    email_ts = timestamp if email_sent else ""
    wa_link = generate_whatsapp_link(session_data.get("phone", ""))

    row = [
        session_data.get("name", ""),
        session_data.get("dob", ""),
        session_data.get("age", ""),
        session_data.get("coverage_status", ""),
        session_data.get("budget_range", ""),
        session_data.get("plan_coverage", ""),
        session_data.get("monthly_premium", ""),
        session_data.get("phone", ""),
        session_data.get("email", ""),
        timestamp,     # Timestamp
        wa_link,       # WhatsappLink (column K)
        email_ts       # Email TimeStamp (column L)
    ]

    all_values = sheet.get_all_values()
    next_row = len(all_values) + 1
    sheet.insert_row(row, next_row)

    print(f"Row added for {session_data.get('name', '')} at row {next_row}")
    return session_data.get("email")

# -----------------------------
# Update Email_sent timestamp
# -----------------------------
def update_email_sent(email):
    """Update the most recent row matching the email with an "Email TimeStamp" value.

    This writes explicitly to column L (index 12) and searches bottom-up for the
    latest row matching the email. Returns the timestamp string when updated,
    otherwise returns None.
    """
    sheet = init_sheet()
    all_values = sheet.get_all_values()

    if not all_values:
        print("No data in sheet to update Email TimeStamp.")
        return None

    # Use explicit column L (12) for Email TimeStamp and column I (9) for Email
    email_col_index = 9
    email_ts_col_index = 12

    # Search from the bottom so we update the most recent matching data row
    for idx in range(len(all_values), 1, -1):  # skip header row (1)
        row = all_values[idx - 1]
        if len(row) >= email_col_index and row[email_col_index - 1].strip() == email.strip():
            email_ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sheet.update_cell(idx, email_ts_col_index, email_ts)
            print(f"Email TimeStamp updated at row {idx}: {email_ts}")
            return email_ts

    print("No matching email found to update Email TimeStamp.")
    return None


# -----------------------------
# Compatibility wrapper
# -----------------------------
def save_session(session_data):
    """Compatibility wrapper for older callers that expect `save_session`.

    This maps keys used by `Medical.py` to the keys expected by
    `save_session_after_email` and calls it.
    """
    mapped = {
        "name": session_data.get("name", ""),
        "dob": session_data.get("dob", ""),
        "age": session_data.get("age", ""),
        # Map older keys to the canonical keys used in the sheet
        "coverage_status": session_data.get("coverage", ""),
        "budget_range": session_data.get("budget", ""),
        "plan_coverage": session_data.get("plan", ""),
        "monthly_premium": session_data.get("premium", ""),
        "phone": session_data.get("phone", ""),
        "email": session_data.get("email", "")
    }

    return save_session_after_email(mapped, email_sent=False)
