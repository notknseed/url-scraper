@echo off
echo ================================================
echo         Website URL Scraper - Launcher
echo ================================================
echo.

:: Quick Python check
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo 🔧 Please run "run_direct.bat" first to setup environment
    echo.
    pause
    exit /b 1
)

:: Check if scraper script exists
if not exist "scrapeURL.py" (
    echo ❌ scrapeURL.py not found!
    echo 📁 Make sure you're in the correct directory
    echo.
    pause
    exit /b 1
)

:: Run the scraper
echo 🚀 Starting Website URL Scraper...
echo.
python scrapeURL.py

echo.
echo 📄 Scraper finished. Check results above.
pause