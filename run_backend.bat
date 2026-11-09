@echo off
echo ======================================================
echo    STARTING LPBANK AI RM COPILOT - BACKEND API
echo ======================================================
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
pause

