#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Find the right Python command
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "Error: Python not found. Install Python 3.10+ from https://www.python.org/downloads/"
    exit 1
fi

$PY -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py