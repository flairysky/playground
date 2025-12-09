@echo off
echo ============================================
echo MathTracker Quick Start Script
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
    echo Done!
    echo.
) else (
    echo [1/5] Virtual environment already exists
    echo.
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo Done!
echo.

echo [3/5] Installing dependencies...
pip install -r requirements.txt
echo Done!
echo.

REM Check if database exists
if not exist "instance\app.db" (
    echo [4/5] Initializing database...
    python init_db.py
    echo Done!
    echo.
) else (
    echo [4/5] Database already exists
    echo.
)

echo [5/5] Starting Flask application...
echo.
echo ============================================
echo App will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo ============================================
echo.

python app.py
