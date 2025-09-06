import sqlite3
import os
from typing import Dict, Any, List

DB_PATH = "ai_email_assistant/emails.db"

def init_db():
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                subject TEXT,
                body TEXT,
                date TEXT,
                sentiment TEXT,
                sentiment_score REAL,
                priority TEXT,
                phones TEXT,
                alternate_emails TEXT,
                requirements TEXT,
                positive_indicators TEXT,
                negative_indicators TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        raise RuntimeError(f"Database initialization failed: {e}")

def insert_email(email_data: Dict[str, Any]):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO emails (
                sender, subject, body, date, sentiment, sentiment_score, priority,
                phones, alternate_emails, requirements, positive_indicators, negative_indicators
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email_data.get("sender"),
            email_data.get("subject"),
            email_data.get("body"),
            email_data.get("date"),
            email_data.get("sentiment"),
            email_data.get("sentiment_score"),
            email_data.get("priority"),
            ",".join(email_data.get("phones", [])),
            ",".join(email_data.get("alternate_emails", [])),
            "|".join(email_data.get("requirements", [])),
            ",".join(email_data.get("positive_indicators", [])),
            ",".join(email_data.get("negative_indicators", []))
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        raise RuntimeError(f"Database insert failed: {e}")

def fetch_emails(limit: int = 50) -> List[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM emails ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        columns = [desc[0] for desc in c.description]
        emails = [dict(zip(columns, row)) for row in rows]
        conn.close()
        return emails
    except Exception as e:
        raise RuntimeError(f"Database fetch failed: {e}")