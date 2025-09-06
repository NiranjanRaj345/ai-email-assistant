import os
from typing import Dict
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_response(email_data: Dict, knowledge_base: str = "") -> str:
    prompt = f"""
You are a professional support assistant. Respond to the following email with empathy and context. Use the knowledge base if relevant.

Email:
From: {email_data.get('sender')}
Subject: {email_data.get('subject')}
Body: {email_data.get('body')}
Sentiment: {email_data.get('sentiment')}
Priority: {email_data.get('priority')}
Requirements: {', '.join(email_data.get('requirements', []))}
Knowledge Base: {knowledge_base}

Reply:
"""
    # OpenRouter
    if OPENROUTER_API_KEY:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        # Use a popular free model, e.g., "openrouter/mistral-7b"
        payload = {
            "model": "openrouter/mistral-7b",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.7
        }
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    # OpenAI
    elif OPENAI_API_KEY:
        import openai
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    # Hugging Face
    elif HUGGINGFACE_API_KEY:
        url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": prompt}
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()[0]["generated_text"].strip()
    # Anthropic
    elif ANTHROPIC_API_KEY:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "model": "claude-2",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.7
        }
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    # Gemini (Google)
    elif GEMINI_API_KEY:
        url = "https://generativelanguage.googleapis.com/v1beta2/models/gemini-pro:generateContent"
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    else:
        raise RuntimeError("No supported API key found. Please set one in your environment.")