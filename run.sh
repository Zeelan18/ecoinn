#!/bin/bash

# ============================================================
# EcoVolt AI - Smart Microgrid System Startup Script
# Run this file to start the application on macOS/Linux
# ============================================================

echo ""
echo "============================================================"
echo "  EcoVolt AI - Smart Microgrid System"
echo "============================================================"
echo ""
echo "Starting Flask application..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $PYTHON_VERSION"
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
python3 -m pip show flask > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "============================================================"
echo "Starting server..."
echo "Access the application at: http://localhost:5000"
echo ""
echo "Demo credentials:"
echo "  Username: demo"
echo "  Password: demo123"
echo "============================================================"
echo ""

# Start the Flask app
python3 app.py
