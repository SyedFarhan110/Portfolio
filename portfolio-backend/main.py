from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr
import os
from dotenv import load_dotenv
import aiosmtplib
from email.message import EmailMessage

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = FastAPI(title="Portfolio Backend API")

# Enable CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Portfolio Backend API is running"}

@app.post("/send-email")
async def send_email(
    name: str = Form(...),
    email: EmailStr = Form(...),
    message: str = Form(...)
):
    if not EMAIL_USER or not EMAIL_PASS:
        raise HTTPException(
            status_code=500,
            detail="Email configuration missing on server"
        )

    email_message = EmailMessage()
    email_message["From"] = EMAIL_USER
    email_message["To"] = EMAIL_USER
    email_message["Reply-To"] = email
    email_message["Subject"] = f"Portfolio Contact: {name}"

    email_message.set_content(
        f"""
New Contact Form Submission

Name: {name}
Email: {email}

Message:
{message}

---
Sent from your portfolio website.
"""
    )

    try:
        await aiosmtplib.send(
            email_message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=EMAIL_USER,
            password=EMAIL_PASS,
        )
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        print("Email error:", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to send email"
        )
