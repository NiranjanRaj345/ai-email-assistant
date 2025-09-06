#!/bin/bash
# Automated backend setup for AI Email Assistant

echo "Installing backend dependencies..."
pip install --user -r requirements.txt || pip install -r requirements.txt

echo "Starting FastAPI server with Uvicorn..."
uvicorn api_server:app --reload