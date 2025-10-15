@echo off
title Healthcare Booking System - Easy Installer
color 0A

echo.
echo ====================================================
echo    HEALTHCARE BOOKING SYSTEM - EASY INSTALLER
echo    For Pratap Bag's Physiotherapy Practice
echo ====================================================
echo.

echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [SUCCESS] Python found!
python --version

echo.
echo [INFO] Checking if virtual environment exists...
if exist ".venv" (
    echo [INFO] Virtual environment found, activating...
    call .venv\Scripts\activate.bat
) else (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    echo [SUCCESS] Virtual environment created!
    echo [INFO] Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo.
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [INFO] Installing required packages...
pip install -r requirements.txt

echo.
echo [INFO] Checking Django installation...
python -c "import django; print(f'Django {django.get_version()} installed successfully!')" 2>nul
if errorlevel 1 (
    echo [ERROR] Django installation failed!
    pause
    exit /b 1
)

echo.
echo [INFO] Running database migrations...
python manage.py migrate

echo.
echo [INFO] Collecting static files...
python manage.py collectstatic --noinput

echo.
echo [INFO] Creating superuser (Admin account)...
echo You will need to create an admin account for the healthcare system.
python manage.py createsuperuser

echo.
echo ====================================================
echo    INSTALLATION COMPLETED SUCCESSFULLY!
echo ====================================================
echo.
echo The Healthcare Booking System is now ready to use!
echo.
echo To start the server:
echo   1. Run: start_server.bat
echo   2. Or manually: python manage.py runserver
echo.
echo Then open your browser and go to:
echo   - Website: http://127.0.0.1:8000
echo   - Admin Panel: http://127.0.0.1:8000/admin
echo.
echo For any issues, check the README.md file.
echo.
pause