@echo off
echo ========================================
echo News Aggregator Setup Script
echo ========================================
echo.

echo [1/6] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [4/6] Running database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo Migrations completed successfully!
echo.

echo [5/6] Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ERROR: Failed to collect static files
    pause
    exit /b 1
)
echo Static files collected successfully!
echo.

echo [6/6] Fetching initial news articles...
python manage.py fetch_feeds
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the development server, run:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000
echo.
pause
