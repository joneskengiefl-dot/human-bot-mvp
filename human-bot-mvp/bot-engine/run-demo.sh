#!/bin/bash
# Run 100 sessions demo script for macOS/Linux

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the demo script
python3 demo_100_sessions.py

# Deactivate virtual environment
deactivate
