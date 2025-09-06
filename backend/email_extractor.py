import re
from typing import Dict

def extract_info(email_data: Dict) -> Dict:
    body = email_data.get("body", "")
    if not body or not isinstance(body, str):
        return {
            "phones": [],
            "alternate_emails": [],
            "requirements": [],
            "positive_indicators": [],
            "negative_indicators": []
        }
    # Extract phone numbers
    phone_pattern = r"(?:\+?\d{1,3}[-.\s]?)?(?:\d{10}|\d{3}[-.\s]\d{3}[-.\s]\d{4})"
    phones = re.findall(phone_pattern, body)
    # Extract alternate emails
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    emails = re.findall(email_pattern, body)
    # Extract requirements/requests (simple heuristic: sentences with "need", "require", "want", "request")
    req_pattern = r"([^.]*\b(need|require|want|request|cannot access|issue|problem)\b[^.]*)"
    requirements = [m[0].strip() for m in re.findall(req_pattern, body, re.IGNORECASE) if m[0].strip()]
    # Sentiment indicators (positive/negative words)
    positive_words = ["thank", "appreciate", "great", "happy", "satisfied"]
    negative_words = ["frustrated", "angry", "disappointed", "problem", "issue", "cannot", "not working"]
    positives = [w for w in positive_words if w in body.lower()]
    negatives = [w for w in negative_words if w in body.lower()]
    sender = email_data.get("sender", "")
    return {
        "phones": [p for p in phones if p],
        "alternate_emails": [e for e in emails if e and e != sender],
        "requirements": requirements,
        "positive_indicators": positives,
        "negative_indicators": negatives
    }