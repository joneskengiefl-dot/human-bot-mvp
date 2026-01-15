#!/bin/bash

echo "Setting up Python environment for Human B.O.T Engine..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Step 0: Cleaning up old logging directory (if exists)..."
if [ -d "logging" ]; then
    echo "Removing old logging directory to avoid conflicts..."
    rm -rf logging
fi

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Upgrading pip..."
python -m pip install --upgrade pip

echo "Step 4: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "Step 5: Installing Playwright browsers..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "WARNING: Playwright installation failed. You may need to run: playwright install-deps chromium"
fi

echo "Step 6: Creating directories..."
mkdir -p data
mkdir -p logs

echo "Step 7: Setting up config..."
if [ ! -f config.yaml ]; then
    cp config.example.yaml config.yaml
    echo "Created config.yaml from example. Please edit it with your settings."
else
    echo "config.yaml already exists. Skipping..."
fi

echo
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo
echo "To run the bot engine:"
echo "  python main.py --sessions 5"
echo
echo "To start the API server:"
echo "  python -m api.server"
echo
