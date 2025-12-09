#!/bin/bash
echo "============================================"
echo "MathTracker Quick Start Script"
echo "============================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[1/5] Creating virtual environment..."
    python3 -m venv venv
    echo "Done!"
    echo ""
else
    echo "[1/5] Virtual environment already exists"
    echo ""
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate
echo "Done!"
echo ""

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt
echo "Done!"
echo ""

# Check if database exists
if [ ! -f "instance/app.db" ]; then
    echo "[4/5] Initializing database..."
    python init_db.py
    echo "Done!"
    echo ""
else
    echo "[4/5] Database already exists"
    echo ""
fi

echo "[5/5] Starting Flask application..."
echo ""
echo "============================================"
echo "App will be available at: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo "============================================"
echo ""

python app.py
