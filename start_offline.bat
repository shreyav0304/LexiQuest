@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo One-time setup is needed. Follow "Run on Windows" in README.md.
    echo After setup, this launcher works without internet.
    pause
    exit /b 1
)
echo Starting LexiQuest on this computer. No internet is needed after setup.
echo Keep this window open. Press Ctrl+C here to stop the app.
".venv\Scripts\python.exe" -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
if errorlevel 1 pause
