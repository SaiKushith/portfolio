
import os
import traceback
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Allow Vercel frontend
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Portfolio backend is live"
    })

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        print("\n========== NEW REQUEST ==========")

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        message = data.get("message", "").strip()

        print("Name:", name)
        print("Email:", email)

        if not name or not email or not message:
            return jsonify({
                "success": False,
                "error": "All fields are required"
            }), 400

        host = os.getenv("EMAIL_HOST")
        port = os.getenv("EMAIL_PORT")
        user = os.getenv("EMAIL_HOST_USER")
        password = os.getenv("EMAIL_HOST_PASSWORD")

        print("HOST:", host)
        print("PORT:", port)
        print("USER:", user)

        if not host:
            return jsonify({
                "success": False,
                "error": "EMAIL_HOST missing"
            }), 500

        if not port:
            return jsonify({
                "success": False,
                "error": "EMAIL_PORT missing"
            }), 500

        if not user:
            return jsonify({
                "success": False,
                "error": "EMAIL_HOST_USER missing"
            }), 500

        if not password:
            return jsonify({
                "success": False,
                "error": "EMAIL_HOST_PASSWORD missing"
            }), 500

        msg = MIMEMultipart()
        msg["From"] = user
        msg["To"] = user
        msg["Subject"] = f"Portfolio Contact - {name}"
        msg["Reply-To"] = email

        body = f"""
Name: {name}

Email: {email}

Message:
{message}
"""

        msg.attach(MIMEText(body, "plain"))

        print("Connecting to SMTP server...")

        with smtplib.SMTP(host, int(port), timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()

            print("Logging into Gmail...")

            server.login(user, password)

            print("Sending email...")

            server.sendmail(
                user,
                user,
                msg.as_string()
            )

        print("EMAIL SENT SUCCESSFULLY")

        return jsonify({
            "success": True,
            "message": "Email sent successfully"
        }), 200

    except Exception as e:
        print("\n========== ERROR ==========")
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )

