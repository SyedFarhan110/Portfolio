# Portfolio Backend API

FastAPI backend for handling contact form submissions.

## Setup

1. **Install Python dependencies** (already done):
   ```bash
   pip install fastapi uvicorn python-multipart email-validator aiosmtplib python-dotenv
   ```

2. **Configure Email Settings**:
   - Open `.env` file
   - Add your Gmail address to `EMAIL_USER`
   - Generate a Gmail App Password and add it to `EMAIL_PASS`

3. **Run the server**:
   ```bash
   python main.py
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

## Gmail App Password Setup

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification if not already enabled
3. Go to App passwords
4. Select "Mail" and "Other (Custom name)"
5. Generate password and copy it
6. Paste it in `.env` file as `EMAIL_PASS`

## API Endpoint

**POST** `/send-email`

Form data:
- `name`: Sender's name
- `email`: Sender's email
- `message`: Message content

Response:
```json
{
  "message": "Email sent successfully!",
  "success": true
}
```

## Testing

Visit http://127.0.0.1:8000 to check if the API is running.

You should see: `{"message": "Portfolio Backend API is running"}`
