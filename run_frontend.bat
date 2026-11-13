@echo off
cd /d "%~dp0"
set PYTHONPATH=%~dp0
echo ======================================================
echo    STARTING LPBANK AI RM COPILOT - STREAMLIT FRONTEND
echo ======================================================
python -m streamlit run frontend/app.py --server.port 8501
pause
