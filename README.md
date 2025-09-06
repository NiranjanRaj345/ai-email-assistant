# AI-Powered Communication Assistant

## Overview

A full-stack solution for automating support email management using AI. Fetches, filters, analyzes, prioritizes, extracts info, generates responses, and displays results on a modern dashboard.

---

## Features

- Fetches emails from Gmail/IMAP/Outlook
- Filters support-related emails by subject
- Sentiment and urgency analysis (AI/LLM)
- Key info extraction (contacts, requirements, indicators)
- Context-aware AI response drafts
- Dashboard with analytics, search, and interactive graphs
- Validation and error handling throughout
- User login for email credentials (no need to edit env files)
- Supports multiple LLM providers (OpenAI, OpenRouter, Hugging Face, Anthropic, Gemini, etc.)

---

## Project Structure

```
ai_email_assistant/
│
├── backend/                # Python FastAPI backend
│   ├── api_server.py       # API endpoints, validation, logging, session-based login
│   ├── email_fetcher.py    # Email retrieval/filtering
│   ├── email_analyzer.py   # Sentiment/priority analysis
│   ├── email_extractor.py  # Info extraction
│   ├── email_db.py         # SQLite DB operations
│   ├── response_generator.py # LLM-powered response generation (multi-provider)
│   ├── requirements.txt    # Backend dependencies
│
├── frontend/               # React/Next.js frontend
│   ├── pages/index.js      # Main dashboard UI
│   ├── pages/login.js      # User login for email credentials
│   ├── components/         # UI components (MainLayout, AnalyticsGraph)
│   ├── README.md           # Frontend instructions
│
├── .env.example            # Sample environment variables
├── .gitignore              # Ignore rules
├── README.md               # Project documentation
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/NiranjanRaj345/ai-email-assistant.git
cd ai-email-assistant
```

### 2. Configure Environment Variables


#### Step 1: Copy `.env.example` to `.env`

- **Linux/macOS:**
  ```bash
  cp .env.example .env
  ```
- **Windows (Command Prompt):**
  ```cmd
  copy .env.example .env
  ```
- **Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```

#### Step 2: Edit `.env` to add your API keys

- Open `.env` in your preferred editor:
  - **Terminal (Linux/macOS):** `nano .env` or `vim .env`
  - **Terminal (Windows):** `notepad .env`
  - **VSCode:** Open `.env` from the file explorer

- Add your API keys for each provider:
  - `OPENAI_API_KEY`
  - `OPENROUTER_API_KEY`
  - `HUGGINGFACE_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `GEMINI_API_KEY`

- You can obtain these keys from your accounts on each provider's website.

- The `.env` file is required for backend to connect to LLMs and for secure session management.

### 3. Backend Setup

```bash
cd backend
bash install_backend.sh
```
This script will automatically install all dependencies and start the FastAPI server.

### 4. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

- Access the dashboard at `http://localhost:3000`
- Login with your email credentials on `/login` page

---

## How It Works

1. **Frontend**: User logs in with email credentials. Dashboard displays filtered emails, analytics, and AI-generated responses.
2. **Backend**: Uses session-based credentials for IMAP login, fetches/filter support emails, analyzes sentiment/priority, extracts info, stores in DB, and exposes APIs.
3. **AI**: Generates context-aware, empathetic replies using the selected LLM provider.

---

## Impact

- Reduces manual workload for support teams
- Ensures faster, empathetic, accurate responses
- Extracts actionable insights
- Improves customer satisfaction

---

## Author

Niranjan Rajkumar