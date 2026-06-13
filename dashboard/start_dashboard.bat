@echo off
REM Quick start script for the Knowledge Tracing Dashboard

echo ============================================================
echo  Knowledge Tracing Analysis Dashboard
echo ============================================================
echo.

echo Checking Streamlit installation...
python -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Streamlit not found!
    echo.
    echo Please install dependencies first:
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo ✓ Streamlit is installed
echo.
echo Starting dashboard...
echo.
echo 📊 The dashboard will open at: http://localhost:8501
echo 💡 Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
streamlit run app.py
pause
