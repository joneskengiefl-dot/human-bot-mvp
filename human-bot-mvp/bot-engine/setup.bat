@echo off
echo Setting up Python environment for Human B.O.T Engine...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Step 0: Cleaning up old logging directory (if exists)...
if exist logging (
    echo Removing old logging directory to avoid conflicts...
    rmdir /s /q logging
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Step 5: Installing Playwright browsers...
playwright install chromium
if errorlevel 1 (
    echo WARNING: Playwright installation failed. You may need to run: playwright install-deps chromium
)

echo Step 6: Creating directories...
if not exist data mkdir data
if not exist logs mkdir logs

echo Step 7: Setting up config...
if not exist config.yaml (
    copy config.example.yaml config.yaml
    echo Created config.yaml from example. Please edit it with your settings.
) else (
    echo config.yaml already exists. Skipping...
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the bot engine:
echo   python main.py --sessions 5
echo.
echo To start the API server:
echo   python -m api.server
echo.
pause
