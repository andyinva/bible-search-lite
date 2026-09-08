@echo off
title Bible Search Lite
REM ===================================================================
REM Bible Search Lite launcher
REM Runs the copy in THIS folder (Documents\Projects\bible-search-lite)
REM through WSL Ubuntu. The window stays open if anything goes wrong so
REM the error message can be read.
REM ===================================================================

REM %~dp0 is the folder this .bat lives in (ends with a backslash)
set PROJECT_DIR=%~dp0

echo Starting Bible Search Lite...

REM --- Make sure WSL is available ---
where wsl >nul 2>&1
if errorlevel 1 (
    echo ERROR: Windows could not find WSL. Is WSL installed?
    pause
    exit /b 1
)

REM --- Try the Ubuntu-24.04 distribution first ---
wsl -d Ubuntu-24.04 bash -c "cd '/mnt/c/Users/Andrew Hopkins/Documents/Projects/bible-search-lite' && python3 bible_search_lite.py"
if not errorlevel 1 exit /b 0

echo.
echo Ubuntu-24.04 did not start the program. Trying the default WSL
echo distribution instead...
echo.

REM --- Fall back to whatever the default WSL distribution is ---
wsl bash -c "cd '/mnt/c/Users/Andrew Hopkins/Documents/Projects/bible-search-lite' && python3 bible_search_lite.py"
if not errorlevel 1 exit /b 0

echo.
echo ERROR: Bible Search Lite could not start. The messages above
echo should say why (for example: distribution name, missing python3,
echo or missing PyQt6 inside WSL).
pause
