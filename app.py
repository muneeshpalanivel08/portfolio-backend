from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()

    first_name = data.get("firstName", "")
    last_name = data.get("lastName", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    message = data.get("message", "")

    # Email content setup
    subject = f"New Contact Form Submission from {first_name} {last_name}"
    body = f"""
    You received a new message from your portfolio contact form:

    Name: {first_name} {last_name}
    Email: {email}
    Phone: {phone}

    Message:
    {message}
    """

    try:
        # Set up the MIME email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        return jsonify({"code": 200, "message": "Email sent successfully"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"code": 500, "message": "Failed to send email"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
