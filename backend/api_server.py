from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from ai_email_assistant.email_db import fetch_emails, insert_email, init_db
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "supersecret"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return JSONResponse({"error": "Missing credentials"}, status_code=400)
    request.session["email"] = email
    request.session["password"] = password
    return {"status": "success"}

@app.get("/emails", response_model=List[Dict])
def get_emails(limit: int = 50, request: Request = None):
    if not isinstance(limit, int) or limit <= 0 or limit > 1000:
        raise HTTPException(status_code=400, detail="Limit must be an integer between 1 and 1000")
    # Use session credentials if available
    email = None
    password = None
    if request and hasattr(request, "session"):
        email = request.session.get("email")
        password = request.session.get("password")
    # Fallback to env if not in session
    if not email:
        email = os.getenv("EMAIL_USER")
    if not password:
        password = os.getenv("EMAIL_PASS")
    if not email or not password:
        raise HTTPException(status_code=401, detail="Email credentials not provided")
    try:
        from ai_email_assistant.email_fetcher import connect_imap, fetch_support_emails
        mail = connect_imap(email, password)
        emails = fetch_support_emails(mail)
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email fetch failed: {e}")

class EmailModel(BaseModel):
    sender: str = Field(..., min_length=3)
    subject: str = Field(..., min_length=3)
    body: str = Field(..., min_length=3)
    date: str = Field(..., min_length=3)
    sentiment: str = Field(..., min_length=3)
    sentiment_score: float
    priority: str = Field(..., min_length=3)
    phones: list = []
    alternate_emails: list = []
    requirements: list = []
    positive_indicators: list = []
    negative_indicators: list = []

@app.post("/emails")
def add_email(email: Dict):
    try:
        validated_email = EmailModel(**email)
        insert_email(validated_email.dict())
        logging.info(f"Inserted email from {validated_email.sender} with subject '{validated_email.subject}'")
        return {"status": "success"}
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=f"Validation error: {ve}")
    except Exception as e:
        logging.error(f"Insert failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
def get_analytics():
    try:
        emails = fetch_emails(1000)
        total = len(emails)
        resolved = sum(1 for e in emails if e.get("priority") == "Not urgent")
        pending = sum(1 for e in emails if e.get("priority") == "Urgent")
        sentiments = {"positive": 0, "negative": 0, "neutral": 0}
        for e in emails:
            s = str(e.get("sentiment", "")).lower()
            if "positive" in s:
                sentiments["positive"] += 1
            elif "negative" in s:
                sentiments["negative"] += 1
            else:
                sentiments["neutral"] += 1
        return {
            "total": total,
            "resolved": resolved,
            "pending": pending,
            "sentiments": sentiments
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics calculation failed: {e}")