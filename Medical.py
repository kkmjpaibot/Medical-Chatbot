from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re
from Googlesheet import save_session
from Email import send_campaign4_email

app = Flask(__name__)

# ---------------- MAIN PAGE ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- DOB VALIDATION ----------------
@app.route("/validate_dob", methods=["POST"])
def validate_dob():
    dob = request.json.get("dob")
    try:
        birth_date = datetime.strptime(dob, "%d/%m/%Y")
        today = datetime.today()

        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )

        if age < 18:
            return jsonify({
                "status": "error",
                "message": "You must be at least 18 years old to proceed."
            })

        if age > 80:
            return jsonify({
                "status": "error",
                "message": "This form is only available for users aged 18 to 80."
            })

        return jsonify({
            "status": "ok",
            "age": age
        })

    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Invalid date format. Use DD/MM/YYYY"
        })


# ---------------- PHONE VALIDATION ----------------
@app.route("/validate_phone", methods=["POST"])
def validate_phone():
    phone = request.json.get("phone")
    pattern = r"^(\+60|0)1[0-9]{8,9}$"

    if phone and re.match(pattern, phone):
        return jsonify({"status": "ok"})

    return jsonify({
        "status": "error",
        "message": "Invalid Malaysian phone number"
    })

# ---------------- EMAIL VALIDATION ----------------
@app.route("/validate_email", methods=["POST"])
def validate_email():
    email = request.json.get("email")
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if email and re.match(pattern, email):
        return jsonify({"status": "ok"})

    return jsonify({
        "status": "error",
        "message": "Invalid email format"
    })

# ---------------- SAVE CHAT SESSION ----------------
@app.route("/save_session", methods=["POST"])
def save_chat_session():
    """
    Receives chatbot data, saves it to Google Sheets,
    and triggers sending Campaign 4 email.
    """
    data = request.json

    try:
        # Map frontend keys to Google Sheet headers
        save_session({
            "name": data.get("name", ""),
            "dob": data.get("dob", ""),
            "age": data.get("age", ""),
            "coverage": data.get("coverage", ""),   # Coverage level column
            "budget": data.get("budget", ""),      # Budget column
            "plan": data.get("plan", ""),          # Coverage Plan column
            "premium": data.get("premium", ""),    # Estimated / Monthly Premium column
            "phone": data.get("phone", ""),
            "email": data.get("email", "")
        })

        # Send email automatically after saving and capture the timestamp
        email_ts = send_campaign4_email({
            "name": data.get("name", ""),
            "dob": data.get("dob", ""),
            "age": data.get("age", ""),
            "coverage": data.get("coverage", ""),
            "budget": data.get("budget", ""),
            "plan": data.get("plan", ""),
            "premium": data.get("premium", ""),
            "phone": data.get("phone", ""),
            "email": data.get("email", "")
        })

        return jsonify({"status": "ok", "email_sent": email_ts})

    except Exception as e:
        print("❌ Error in saving session or sending email:", str(e))
        return jsonify({
            "status": "error",
            "message": "Failed to save data or send email"
        })

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
