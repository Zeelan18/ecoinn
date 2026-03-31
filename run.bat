@echo off
REM ============================================================
REM EcoVolt AI - Smart Microgrid System Startup Script
REM Run this file to start the application on Windows
REM ============================================================

title EcoVolt AI - Smart Microgrid System
color 0A

echo.
echo ============================================================
echo   EcoVolt AI - Smart Microgrid System
echo ============================================================
echo.
echo Starting Flask application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -m pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ============================================================
echo Starting server...
echo Access the application at: http://localhost:5000
echo.
echo Demo credentials:
echo   Username: demo
echo   Password: demo123
echo ============================================================
echo.

REM Start the Flask app
python app.py

pause
