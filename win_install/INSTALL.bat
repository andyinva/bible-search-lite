@echo off
REM Bible Search Lite - Easy Installer Launcher
REM This batch file launches the PowerShell installer

echo ================================================
echo Bible Search Lite - Offline Installer
echo ================================================
echo.
echo This will launch the PowerShell installer.
echo.
echo IMPORTANT: This must be run AS ADMINISTRATOR!
echo.
echo If you see errors, right-click this file and
echo select "Run as Administrator"
echo.
pause

REM Check if running as admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator - Good!
    echo.
) else (
    echo ERROR: Not running as Administrator!
    echo.
    echo Please right-click this file and select:
    echo "Run as Administrator"
    echo.
    pause
    exit /b 1
)

REM Launch PowerShell installer
echo Launching installer...
echo.
powershell.exe -ExecutionPolicy Bypass -File "%~dp002_install_offline.ps1"

echo.
echo Installation script finished.
pause
