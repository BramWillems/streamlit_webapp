@echo off
REM Setup script to install dashboard dependencies

echo ============================================================
echo  Knowledge Tracing Dashboard - Setup
echo ============================================================
echo.

echo This script will install all required packages for the dashboard.
echo.

set /p CONFIRM="Continue with installation? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Setup cancelled.
    exit /b 0
)

echo.
echo Installing packages...
echo.

pip install -r requirements.txt

echo.
echo ============================================================
if %errorlevel% equ 0 (
    echo ✓ Setup complete!
    echo.
    echo Next steps:
    echo   1. Run start_dashboard.bat to launch the dashboard
    echo   2. OR run: streamlit run app.py
    echo.
) else (
    echo ERROR: Installation failed!
    echo Please check your pip installation and try again.
    echo.
)

pause
