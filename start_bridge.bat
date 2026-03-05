@echo off
setlocal
cd /d %~dp0

if not exist .venv (
    python -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

echo Starting Undertale save-file bridge...
python bridge.py %*
pause
