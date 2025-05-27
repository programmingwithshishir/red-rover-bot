@echo off
setlocal

REM Step 1: Create virtual environment
python -m venv virt
if errorlevel 1 (
    echo Failed to create virtual environment.
    goto :rollback
)

REM Step 2: Activate virtual environment
call virt\Scripts\activate
if errorlevel 1 (
    echo Failed to activate virtual environment.
    goto :rollback
)

REM Step 3: Install dependencies from requirements.txt
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    goto :rollback
)

REM Step 4: Install Playwright dependencies
playwright install chromium
if errorlevel 1 (
    echo Failed to install Playwright browsers.
    goto :rollback
)

echo Environment setup complete.
echo Press Enter to continue...
pause >nul
goto :eof

:rollback
echo Rolling back setup...
if exist virt (
    rmdir /s /q virt
    echo Virtual environment 'virt' deleted.
)
echo Rollback complete.
echo Press Enter to continue...
pause >nul
exit /b 1