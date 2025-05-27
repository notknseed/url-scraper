@echo off
echo ================================================
echo     Website URL Scraper - Smart Launcher (32-bit)
echo ================================================
echo.

:: Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Auto-installing Python...
    goto :install_python
) else (
    echo Python found!
    goto :install_packages
)

:install_python
echo.
echo Downloading Python 3.11 installer (32-bit)...
powershell -Command "try { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9.exe' -OutFile 'python_installer.exe' -UseBasicParsing } catch { Write-Host 'Download failed'; exit 1 }"

if not exist "python_installer.exe" (
    echo Failed to download Python installer!
    echo Please install Python manually from: https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    goto :error_end
)

echo Installing Python (this may take a few minutes)...
echo Please wait...
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Wait for installation
timeout /t 45 /nobreak >nul

:: Clean up installer
if exist "python_installer.exe" del "python_installer.exe"

:: Refresh PATH
echo Refreshing environment...
call refreshenv.cmd >nul 2>&1

:: Check if Python is now available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python installation completed but not detected in PATH
    echo Please restart this script or reboot your computer
    goto :error_end
)

echo Python installation successful!

:install_packages
echo.
echo Installing required packages...
pip install --upgrade pip
pip install requests beautifulsoup4 lxml

if errorlevel 1 (
    echo Package installation failed!
    goto :error_end
)

echo.
echo All packages installed successfully!
echo.
echo ✅ Setup complete! 
echo 🚀 To run the scraper, use: python scrapeURL.py
echo 📝 Or double-click run_scraper.bat
goto :normal_end

:error_end
echo.
echo Installation failed! Please try running as Administrator
echo or install Python manually from https://python.org/downloads/
pause
exit /b 1

:normal_end
echo.
pause