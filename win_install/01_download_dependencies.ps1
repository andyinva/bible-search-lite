# Bible Search Lite - Offline Installer Dependency Downloader
# Run this script on an INTERNET-CONNECTED PC to download all required files
# Then copy the entire win_install folder to USB drive

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Bible Search Lite - Dependency Downloader" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Create subdirectories
$baseDir = $PSScriptRoot
$pythonDir = Join-Path $baseDir "python"
$pipPackagesDir = Join-Path $baseDir "pip_packages"

Write-Host "Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $pythonDir | Out-Null
New-Item -ItemType Directory -Force -Path $pipPackagesDir | Out-Null

# Python version to download
$pythonVersion = "3.12.1"
$pythonInstallerUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe"
$pythonInstallerPath = Join-Path $pythonDir "python-installer.exe"

# Download Python installer
Write-Host ""
Write-Host "Step 1: Downloading Python $pythonVersion installer..." -ForegroundColor Green
try {
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath -UseBasicParsing
    Write-Host "  ✓ Python installer downloaded: $('{0:N2} MB' -f ((Get-Item $pythonInstallerPath).Length / 1MB))" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to download Python installer: $_" -ForegroundColor Red
    exit 1
}

# Install Python temporarily to download pip packages
Write-Host ""
Write-Host "Step 2: Installing Python temporarily to download pip packages..." -ForegroundColor Green
$tempPythonDir = Join-Path $env:TEMP "BibleSearchPython"
Write-Host "  Installing to: $tempPythonDir" -ForegroundColor Gray

# Install Python silently
$installArgs = "/quiet InstallAllUsers=0 PrependPath=0 Include_test=0 TargetDir=`"$tempPythonDir`""
Start-Process -FilePath $pythonInstallerPath -ArgumentList $installArgs -Wait -NoNewWindow

# Wait a moment for installation to complete
Start-Sleep -Seconds 5

$pythonExe = Join-Path $tempPythonDir "python.exe"
$pipExe = Join-Path $tempPythonDir "Scripts\pip.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "  ✗ Python installation failed!" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Python installed temporarily" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Step 3: Upgrading pip..." -ForegroundColor Green
& $pythonExe -m pip install --upgrade pip --quiet
Write-Host "  ✓ pip upgraded" -ForegroundColor Green

# Download PyQt6 and dependencies
Write-Host ""
Write-Host "Step 4: Downloading PyQt6 and all dependencies..." -ForegroundColor Green
Write-Host "  This may take several minutes..." -ForegroundColor Gray

$packages = @(
    "PyQt6",
    "PyQt6-Qt6",
    "PyQt6-sip"
)

foreach ($package in $packages) {
    Write-Host "  Downloading $package..." -ForegroundColor Yellow
    & $pipExe download $package --dest $pipPackagesDir --platform win_amd64 --python-version 312 --only-binary=:all:
}

Write-Host "  ✓ All packages downloaded" -ForegroundColor Green

# Clean up temporary Python installation
Write-Host ""
Write-Host "Step 5: Cleaning up temporary Python installation..." -ForegroundColor Green
Remove-Item -Path $tempPythonDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  ✓ Cleanup complete" -ForegroundColor Green

# Create version info file
$versionInfo = @"
Bible Search Lite - Offline Installer Package
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Contents:
- Python $pythonVersion installer
- PyQt6 and dependencies (offline pip packages)

Installation Instructions:
1. Copy this entire win_install folder to USB drive
2. On target PC, run: 02_install_offline.ps1
"@

Set-Content -Path (Join-Path $baseDir "package_info.txt") -Value $versionInfo

# Summary
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "DOWNLOAD COMPLETE!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Downloaded files:" -ForegroundColor Yellow
Write-Host "  Python installer: $('{0:N2} MB' -f ((Get-Item $pythonInstallerPath).Length / 1MB))" -ForegroundColor White
$pipPackagesSize = (Get-ChildItem $pipPackagesDir -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "  Pip packages: $('{0:N2} MB' -f $pipPackagesSize)" -ForegroundColor White
Write-Host ""
Write-Host "Total package size: $('{0:N2} MB' -f (((Get-Item $pythonInstallerPath).Length / 1MB) + $pipPackagesSize))" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Copy the entire 'win_install' folder to a USB drive" -ForegroundColor White
Write-Host "  2. On the target PC (offline), run: 02_install_offline.ps1" -ForegroundColor White
Write-Host ""
