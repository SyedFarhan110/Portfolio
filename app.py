from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# Allow only your GitHub Pages domain (frontend)
CORS(app, resources={r"/*": {"origins": "https://syedfarhan110.github.io/Portfolio/"}})

# Email configuration (use environment variables in Render)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("EMAIL_USER")        # Gmail address from Render environment
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD") # Gmail App Password from Render environment


@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"}), 200


@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"status": "error", "message": "All fields are required"}), 400

        # Create email
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = SENDER_EMAIL  # send to yourself
        msg["Subject"] = f"Portfolio Contact from {name}"

        body = f"""
        New contact form submission:

        Name: {name}
        Email: {email}
        Message: {message}
        """
        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send email
        server.send_message(msg)
        server.quit()

        return jsonify({"status": "success", "message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # Render provides PORT automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
