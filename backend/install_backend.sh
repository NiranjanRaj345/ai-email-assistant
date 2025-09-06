#!/bin/bash
# Automated backend setup for AI Email Assistant

echo "Installing backend dependencies..."
python3 -m pip install --user -r requirements.txt || python3 -m pip install -r requirements.txt

echo "Checking FastAPI installation..."
python3 -c "import fastapi" 2>/dev/null || {
  echo "FastAPI not found, trying to install globally and for user..."
  python3 -m pip install fastapi
  python3 -m pip install --user fastapi
  export PYTHONPATH="$HOME/.local/lib/python3.13/site-packages:$PYTHONPATH"
}

echo "Checking Uvicorn installation..."
python3 -c "import uvicorn" 2>/dev/null || {
  echo "Uvicorn not found, trying to install globally and for user..."
  python3 -m pip install uvicorn
  python3 -m pip install --user uvicorn
  export PYTHONPATH="$HOME/.local/lib/python3.13/site-packages:$PYTHONPATH"
}

echo "Starting FastAPI server with Uvicorn..."
python3 -m uvicorn api_server:app --reload