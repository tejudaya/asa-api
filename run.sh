#!/usr/bin/env bash
set -euo pipefail

# Create venv if missing
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Run the FastAPI server
exec uvicorn server:app --host 0.0.0.0 --port 8000 --reload
