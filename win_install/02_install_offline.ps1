# Bible Search Lite - Offline Installer
# Run this script on the TARGET PC (can be offline)
# Requires Administrator privileges

#Requires -RunAsAdministrator

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Bible Search Lite - Offline Installer" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Set paths
$baseDir = $PSScriptRoot
$pythonDir = Join-Path $baseDir "python"
$pipPackagesDir = Join-Path $baseDir "pip_packages"
$pythonInstallerPath = Join-Path $pythonDir "python-installer.exe"

# Verify files exist
Write-Host "Step 1: Verifying installation files..." -ForegroundColor Green
$missingFiles = @()

if (-not (Test-Path $pythonInstallerPath)) {
    $missingFiles += "Python installer"
}
if (-not (Test-Path $pipPackagesDir)) {
    $missingFiles += "Pip packages directory"
}

if ($missingFiles.Count -gt 0) {
    Write-Host "  ✗ Missing files:" -ForegroundColor Red
    $missingFiles | ForEach-Object { Write-Host "    - $_" -ForegroundColor Red }
    Write-Host ""
    Write-Host "Please run 01_download_dependencies.ps1 first on a PC with internet!" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "  ✓ All required files found" -ForegroundColor Green

# Ask for installation directory
Write-Host ""
Write-Host "Step 2: Choose installation location..." -ForegroundColor Green
$defaultInstallDir = Join-Path $env:LOCALAPPDATA "Programs\BibleSearchLite"
Write-Host "  Default: $defaultInstallDir" -ForegroundColor Gray
$customDir = Read-Host "  Press Enter for default, or type custom path"

if ([string]::IsNullOrWhiteSpace($customDir)) {
    $installDir = $defaultInstallDir
} else {
    $installDir = $customDir
}

Write-Host "  Installing to: $installDir" -ForegroundColor Cyan

# Install Python
Write-Host ""
Write-Host "Step 3: Installing Python..." -ForegroundColor Green
Write-Host "  This may take a few minutes..." -ForegroundColor Gray

$pythonInstallDir = Join-Path $installDir "Python"
New-Item -ItemType Directory -Force -Path $pythonInstallDir | Out-Null

# Install Python silently to custom directory
$installArgs = "/quiet InstallAllUsers=0 PrependPath=0 Include_test=0 TargetDir=`"$pythonInstallDir`""
$process = Start-Process -FilePath $pythonInstallerPath -ArgumentList $installArgs -Wait -PassThru -NoNewWindow

if ($process.ExitCode -ne 0) {
    Write-Host "  ✗ Python installation failed with exit code: $($process.ExitCode)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Wait for installation to settle
Start-Sleep -Seconds 3

$pythonExe = Join-Path $pythonInstallDir "python.exe"
$pipExe = Join-Path $pythonInstallDir "Scripts\pip.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "  ✗ Python executable not found after installation!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "  ✓ Python installed successfully" -ForegroundColor Green

# Install PyQt6 from offline packages
Write-Host ""
Write-Host "Step 4: Installing PyQt6 and dependencies..." -ForegroundColor Green

$wheelFiles = Get-ChildItem -Path $pipPackagesDir -Filter "*.whl"
Write-Host "  Found $($wheelFiles.Count) package(s) to install" -ForegroundColor Gray

foreach ($wheel in $wheelFiles) {
    Write-Host "  Installing $($wheel.Name)..." -ForegroundColor Yellow
    & $pipExe install $wheel.FullName --no-index --no-deps --quiet
}

Write-Host "  ✓ All packages installed" -ForegroundColor Green

# Copy Bible Search Lite application
Write-Host ""
Write-Host "Step 5: Installing Bible Search Lite application..." -ForegroundColor Green

$appInstallDir = Join-Path $installDir "BibleSearchLite"
New-Item -ItemType Directory -Force -Path $appInstallDir | Out-Null

# Copy application files (assuming they're in parent directory)
$appSourceDir = Join-Path $baseDir ".."
$filesToCopy = @(
    "bible_search.py",
    "bible_search_lite.py",
    "bible_search_service.py",
    "subject_manager.py",
    "subject_verse_manager.py",
    "subject_comment_manager.py",
    "VERSION.txt"
)

$foldersToC = @(
    "bible_search_ui",
    "database"
)

# Copy files
foreach ($file in $filesToCopy) {
    $sourcePath = Join-Path $appSourceDir $file
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath -Destination $appInstallDir -Force
        Write-Host "  Copied: $file" -ForegroundColor Gray
    }
}

# Copy folders
foreach ($folder in $foldersToC) {
    $sourcePath = Join-Path $appSourceDir $folder
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath -Destination $appInstallDir -Recurse -Force
        Write-Host "  Copied: $folder\" -ForegroundColor Gray
    }
}

Write-Host "  ✓ Application files installed" -ForegroundColor Green

# Create launcher script
Write-Host ""
Write-Host "Step 6: Creating launcher..." -ForegroundColor Green

$launcherScript = Join-Path $installDir "Launch Bible Search Lite.bat"
$launcherContent = @"
@echo off
cd /d "$appInstallDir"
"$pythonExe" bible_search_lite.py
pause
"@

Set-Content -Path $launcherScript -Value $launcherContent

Write-Host "  ✓ Launcher created" -ForegroundColor Green

# Create desktop shortcut
Write-Host ""
Write-Host "Step 7: Creating desktop shortcut..." -ForegroundColor Green

$WshShell = New-Object -ComObject WScript.Shell
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "Bible Search Lite.lnk"
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $launcherScript
$Shortcut.WorkingDirectory = $appInstallDir
$Shortcut.Description = "Bible Search Lite"
$Shortcut.Save()

Write-Host "  ✓ Desktop shortcut created" -ForegroundColor Green

# Create uninstaller
Write-Host ""
Write-Host "Step 8: Creating uninstaller..." -ForegroundColor Green

$uninstallerPath = Join-Path $installDir "Uninstall.ps1"
$uninstallerContent = @"
# Bible Search Lite Uninstaller
Write-Host "Uninstalling Bible Search Lite..." -ForegroundColor Yellow
Remove-Item -Path "$installDir" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$shortcutPath" -Force -ErrorAction SilentlyContinue
Write-Host "Bible Search Lite has been uninstalled." -ForegroundColor Green
Read-Host "Press Enter to exit"
"@

Set-Content -Path $uninstallerPath -Value $uninstallerContent

Write-Host "  ✓ Uninstaller created" -ForegroundColor Green

# Installation complete
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installation Summary:" -ForegroundColor Yellow
Write-Host "  Location: $installDir" -ForegroundColor White
Write-Host "  Python: $pythonInstallDir" -ForegroundColor White
Write-Host "  Application: $appInstallDir" -ForegroundColor White
Write-Host ""
Write-Host "To launch Bible Search Lite:" -ForegroundColor Yellow
Write-Host "  - Double-click the desktop shortcut" -ForegroundColor White
Write-Host "  - OR run: $launcherScript" -ForegroundColor White
Write-Host ""
Write-Host "To uninstall:" -ForegroundColor Yellow
Write-Host "  Run: $uninstallerPath" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"
