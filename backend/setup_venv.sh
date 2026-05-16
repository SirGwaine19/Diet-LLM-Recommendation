#!/bin/bash
# Run from backend/: bash setup_venv.sh
# Then: source venv/bin/activate && alembic upgrade head && uvicorn app.main:app --reload

set -e
cd "$(dirname "$0")"
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi
echo "Activating and installing dependencies..."
. venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "Done. Run: source venv/bin/activate && alembic upgrade head && uvicorn app.main:app --reload"
