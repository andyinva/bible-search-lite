# Bible Search Lite - Offline Windows Installer

This package allows you to install Bible Search Lite on a Windows 11 PC that has **NO internet connection**.

## Overview

The offline installation is a two-step process:

1. **Download Phase** (on a PC with internet)
2. **Install Phase** (on the target offline PC)

---

## Step 1: Download Dependencies (Internet-Connected PC)

### Requirements
- Windows 10/11
- Internet connection
- PowerShell 5.1 or later

### Instructions

1. **Open PowerShell** (does not need to be Administrator)

2. **Navigate to the win_install directory:**
   ```powershell
   cd path\to\bible-search-lite\win_install
   ```

3. **Fix execution policy (if needed):**

   If you get an error about "execution policy", run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   **OR** bypass for just this one script:
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File .\01_download_dependencies.ps1
   ```

   Then skip to step 5.

4. **Run the download script:**
   ```powershell
   .\01_download_dependencies.ps1
   ```

5. **What it downloads:**
   - Python 3.12.1 installer (~25 MB)
   - PyQt6 and all dependencies (~50-60 MB)
   - Total: ~80-85 MB

6. **Wait for completion** (typically 5-10 minutes depending on internet speed)

7. **Copy to USB drive:**
   - Copy the entire `win_install` folder to a USB drive
   - The folder structure should look like:
     ```
     win_install/
     ├── 01_download_dependencies.ps1
     ├── 02_install_offline.ps1
     ├── README.md
     ├── python/
     │   └── python-installer.exe
     └── pip_packages/
         ├── PyQt6-*.whl
         ├── PyQt6_Qt6-*.whl
         └── PyQt6_sip-*.whl
     ```

---

## Step 2: Install on Offline PC

### Requirements
- Windows 10/11 (offline or online - doesn't matter)
- Administrator privileges
- USB drive with downloaded dependencies

### Instructions

1. **Insert USB drive** into the target PC

2. **Open PowerShell as Administrator:**
   - Press `Win + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

3. **Navigate to the USB drive:**
   ```powershell
   cd E:\win_install  # Replace E: with your USB drive letter
   ```

4. **Run the installer:**
   ```powershell
   .\02_install_offline.ps1
   ```

5. **Follow the prompts:**
   - Choose installation location (default: `C:\Users\YourName\AppData\Local\Programs\BibleSearchLite`)
   - Wait for Python installation (2-3 minutes)
   - Wait for package installation (1-2 minutes)
   - Wait for application installation (30 seconds)

6. **Installation complete!**
   - A desktop shortcut will be created
   - Double-click "Bible Search Lite" to launch

---

## Installation Details

### What Gets Installed

1. **Python 3.12.1**
   - Installed to: `{InstallDir}\Python\`
   - Self-contained, won't affect system Python
   - Does NOT modify system PATH

2. **PyQt6**
   - Installed to Python's site-packages
   - Includes PyQt6-Qt6 and PyQt6-sip

3. **Bible Search Lite Application**
   - Installed to: `{InstallDir}\BibleSearchLite\`
   - Includes database, UI modules, and all Python files

4. **Launcher Script**
   - Location: `{InstallDir}\Launch Bible Search Lite.bat`
   - Desktop shortcut created automatically

5. **Uninstaller**
   - Location: `{InstallDir}\Uninstall.ps1`

### Default Installation Location

```
C:\Users\{YourName}\AppData\Local\Programs\BibleSearchLite\
├── Python\                          # Python 3.12.1 installation
│   ├── python.exe
│   ├── Scripts\
│   └── Lib\
├── BibleSearchLite\                 # Application files
│   ├── bible_search_lite.py
│   ├── bible_search.py
│   ├── bible_search_ui\
│   └── database\
├── Launch Bible Search Lite.bat     # Launcher
└── Uninstall.ps1                    # Uninstaller
```

---

## Troubleshooting

### "Execution Policy" Error

If you see an error about execution policy when running PowerShell scripts:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try running the script again.

### "Not Run as Administrator" Error

The installer **must** be run as Administrator. Make sure you:
1. Right-click PowerShell
2. Select "Run as Administrator"

### Python Installation Fails

If Python installation fails:
1. Check you have enough disk space (~500 MB free)
2. Make sure no other Python installer is running
3. Try running the installer again

### Missing Application Files

If you see "Missing files" error during installation:
1. Make sure you copied the **entire** `win_install` folder to USB
2. Make sure the USB drive is properly mounted
3. Check that `01_download_dependencies.ps1` completed successfully

### Application Won't Launch

If the desktop shortcut doesn't work:
1. Try running the launcher directly: `{InstallDir}\Launch Bible Search Lite.bat`
2. Check that Python installed correctly: `{InstallDir}\Python\python.exe --version`
3. Check error messages in the console window

---

## Uninstalling

To uninstall Bible Search Lite:

1. **Open PowerShell as Administrator**

2. **Run the uninstaller:**
   ```powershell
   cd "C:\Users\{YourName}\AppData\Local\Programs\BibleSearchLite"
   .\Uninstall.ps1
   ```

This will:
- Remove all installed files
- Remove the Python installation
- Remove the desktop shortcut

---

## Technical Details

### Why Offline Installation?

This installer is designed for:
- Air-gapped systems (high security environments)
- Computers without internet access
- Situations where you want complete control over what's installed

### Security

- All files are downloaded from official sources (python.org, PyPI)
- Python installer is the official Microsoft Store version
- No executables are modified or repackaged
- You can verify the Python installer hash against python.org

### Package Versions

| Package | Version | Size |
|---------|---------|------|
| Python | 3.12.1 | ~25 MB |
| PyQt6 | Latest | ~40 MB |
| PyQt6-Qt6 | Latest | ~10 MB |
| PyQt6-sip | Latest | ~500 KB |

### System Requirements

- Windows 10 version 1809 or later
- Windows 11 (any version)
- 64-bit processor
- 500 MB free disk space
- Administrator privileges (for installation only)

---

## FAQ

**Q: Can I install to a different location?**
A: Yes! The installer will prompt you for a custom location.

**Q: Will this affect my existing Python installation?**
A: No. This is a completely isolated installation that won't touch your system Python.

**Q: Can I move the installation after installing?**
A: Not recommended. The launcher paths are hard-coded. If you need to move it, re-run the installer to the new location.

**Q: How do I update Bible Search Lite?**
A: Download the latest version, run the downloader again, then re-run the installer.

**Q: Can I install on Windows 10?**
A: Yes! This works on Windows 10 (1809 or later) and Windows 11.

**Q: Do I need to keep the USB drive after installation?**
A: No. Once installed, you can remove the USB drive.

**Q: How much space does it use?**
A: Approximately 250-300 MB total (Python + PyQt6 + Bible Search Lite).

---

## Support

For issues or questions:
- Check the Troubleshooting section above
- Review the main Bible Search Lite documentation
- Check the GitHub repository: https://github.com/andyinva/bible-search-lite

---

## License

Bible Search Lite is open source software.
See the LICENSE file in the main repository for details.
