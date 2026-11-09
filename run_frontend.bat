@echo off
echo ======================================================
echo    STARTING LPBANK AI RM COPILOT - STREAMLIT FRONTEND
echo ======================================================
set PYTHONPATH=%CD%
streamlit run frontend/app.py --server.port 8501
pause

