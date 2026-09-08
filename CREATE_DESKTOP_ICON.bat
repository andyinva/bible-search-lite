@echo off
title Create Bible Search Lite Desktop Icon
REM ===================================================================
REM Double-click this file ONCE to (re)create the Bible Search Lite
REM shortcut on the desktop. It uses Windows' own shortcut engine, so
REM the icon and double-click behavior are guaranteed to work.
REM It also clears the 'downloaded from the internet' flag from the
REM launcher and icon files so Windows runs them without complaints.
REM ===================================================================

REM Remove the 'blocked' internet flag from the project launcher files
powershell -NoProfile -Command "Get-ChildItem -Path '%~dp0run_bible_search_win.bat','%~dp0bible_search_lite.ico' | Unblock-File"

REM Build the desktop shortcut (overwrites any old one with this name)
powershell -NoProfile -Command "$d=[Environment]::GetFolderPath('Desktop'); $w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut($d+'\Bible Search Lite.lnk'); $s.TargetPath='%~dp0run_bible_search_win.bat'; $s.WorkingDirectory='%~dp0'; $s.IconLocation='%~dp0bible_search_lite.ico,0'; $s.WindowStyle=7; $s.Description='Bible Search Lite'; $s.Save(); Write-Host 'Desktop shortcut created:' ($d+'\Bible Search Lite.lnk')"

echo.
echo Done! Look for "Bible Search Lite" on your desktop.
pause
