from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr
import os
from dotenv import load_dotenv
import aiosmtplib
from email.message import EmailMessage

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = FastAPI()

# Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
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
    if not name or not email or not message:
        raise HTTPException(status_code=400, detail="All fields are required")
    
    if not EMAIL_USER or not EMAIL_PASS:
        raise HTTPException(status_code=500, detail="Email configuration missing")

    email_message = EmailMessage()
    email_message["From"] = EMAIL_USER
    email_message["Reply-To"] = email
    email_message["To"] = EMAIL_USER
    email_message["Subject"] = f"Portfolio Contact: New message from {name}"
    
    # Create a nicely formatted email body
    body = f"""
    New Contact Form Submission
    
    From: {name}
    Email: {email}
    
    Message:
    {message}
    
    ---
    This message was sent from your portfolio contact form.
    Reply to: {email}
    """
    
    email_message.set_content(body)

    try:
        await aiosmtplib.send(
            email_message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username=EMAIL_USER,
            password=EMAIL_PASS,
        )
        return {"message": "Email sent successfully!", "success": True}
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email. Please try again later.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
