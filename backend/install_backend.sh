#!/bin/bash
# Automated backend setup for AI Email Assistant

echo "Installing backend dependencies..."
python3 -m pip install --user -r requirements.txt || python3 -m pip install -r requirements.txt

echo "Checking FastAPI installation..."
python3 -c "import fastapi" 2>/dev/null || { echo "FastAPI not found, trying to install again..."; python3 -m pip install --user fastapi || python3 -m pip install fastapi; }

echo "Starting FastAPI server with Uvicorn..."
uvicorn api_server:app --reload