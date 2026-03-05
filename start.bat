@echo off
setlocal
cd /d %~dp0
py -m pip install -r requirements.txt
start "" py app.py
timeout /t 2 /nobreak >nul
start http://localhost:3000
py bridge.py
