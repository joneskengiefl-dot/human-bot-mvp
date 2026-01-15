@echo off
REM Run 100 sessions demo script for Windows

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the demo script
python demo_100_sessions.py

REM Deactivate virtual environment
deactivate
