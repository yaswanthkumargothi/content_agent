@echo off
setlocal enabledelayedexpansion

:: Check Python installation
python --version > NUL 2>&1
if errorlevel 1 (
    echo Python is not found. Please install Python and add it to PATH
    pause
    exit /b 1
)

:: Create fresh virtual environment
echo Creating virtual environment...
if exist venv (
    rd /s /q venv 2>nul || powershell -Command "Remove-Item -Recurse -Force venv"
)
python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip and setuptools
echo Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel

:: Install duckduckgo-search first
echo Installing duckduckgo-search...
pip install duckduckgo-search>=4.1.1

:: Install remaining requirements
echo Installing other requirements...
pip install -r requirements.txt

echo Setup completed successfully!
pause
