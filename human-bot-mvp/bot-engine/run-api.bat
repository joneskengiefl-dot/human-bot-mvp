@echo off
REM Run API server script for Windows

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the API server
python -m api.server

REM Deactivate virtual environment
deactivate
