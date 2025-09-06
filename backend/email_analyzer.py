from typing import Dict
from transformers import pipeline

# Load sentiment analysis pipeline (can be replaced with custom model)
try:
    sentiment_pipeline = pipeline("sentiment-analysis")
except Exception as e:
    raise RuntimeError(f"Failed to load sentiment analysis pipeline: {e}")

def analyze_email(email_data: Dict) -> Dict:
    body = email_data.get("body", "")
    if not body or not isinstance(body, str):
        return {"sentiment": "neutral", "sentiment_score": 0.0, "priority": "Not urgent"}
    try:
        sentiment_result = sentiment_pipeline(body)[0]
        sentiment = sentiment_result.get("label", "neutral")
        score = sentiment_result.get("score", 0.0)
    except Exception:
        sentiment = "neutral"
        score = 0.0

    # Priority detection based on keywords
    priority_keywords = ["immediately", "critical", "urgent", "cannot access", "asap", "important"]
    priority = "Not urgent"
    if any(kw in body.lower() for kw in priority_keywords):
        priority = "Urgent"

    return {
        "sentiment": sentiment,
        "sentiment_score": score,
        "priority": priority
    }