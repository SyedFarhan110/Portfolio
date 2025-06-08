from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('EMAIL_USER')  # Your Gmail address
SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Your Gmail app password

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = SENDER_EMAIL  # Send to yourself
        msg['Subject'] = f"Portfolio Contact from {name}"
        
        # Email body
        body = f"""
        New contact form submission:
        
        Name: {name}
        Email: {email}
        Message: {message}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return jsonify({"status": "success", "message": "Email sent successfully"}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False) 