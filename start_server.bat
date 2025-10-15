@echo off
title Healthcare Booking System - Server
color 0B

echo.
echo ====================================================
echo    HEALTHCARE BOOKING SYSTEM - SERVER STARTUP
echo    For Pratap Bag's Physiotherapy Practice
echo ====================================================
echo.

echo [INFO] Activating virtual environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo [SUCCESS] Virtual environment activated!
) else (
    echo [ERROR] Virtual environment not found!
    echo Please run install.bat first to set up the system.
    pause
    exit /b 1
)

echo.
echo [INFO] Checking for pending migrations...
python manage.py showmigrations --plan | findstr "\[ \]" >nul
if not errorlevel 1 (
    echo [INFO] Applying pending migrations...
    python manage.py migrate
)

echo.
echo [INFO] Starting Django development server...
echo.
echo ====================================================
echo    SERVER IS STARTING...
echo ====================================================
echo.
echo Website will be available at: http://127.0.0.1:8000
echo Admin Panel will be available at: http://127.0.0.1:8000/admin
echo.
echo Press Ctrl+C to stop the server
echo ====================================================
echo.

python manage.py runserver 127.0.0.1:8000