@echo off

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Streamlit app
streamlit run skin_ai_demo/app.py

pause
