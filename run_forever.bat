@echo off
REM 🚀 Smart Interview Prep Tool - FOREVER RUNNER
REM This script keeps your app running FOREVER with auto-restart

title Smart Interview Prep Tool - PRODUCTION SERVER

echo.
echo ========================================
echo 🎯 SMART INTERVIEW PREP TOOL
echo 🚀 BULLETPROOF PRODUCTION SERVER
echo ========================================
echo.

cd /d "%~dp0"

:start_server
echo 🌟 Starting production server...
echo 📅 %date% %time%
echo.

REM Run the production server
python run_production.py

REM If the server stops, wait 5 seconds and restart
echo.
echo ⚠️  Server stopped! Auto-restarting in 5 seconds...
echo 📅 %date% %time%
timeout /t 5 /nobreak >nul

REM Check if user wants to stop (Ctrl+C handling)
if errorlevel 1 (
    echo.
    echo 👋 Server stopped by user
    pause
    exit
)

echo 🔄 Restarting server...
goto start_server