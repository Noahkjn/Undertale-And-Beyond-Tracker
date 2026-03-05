#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "Starting Undertale save-file bridge..."
python bridge.py "$@"
