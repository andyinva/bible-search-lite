# Bible Search Lite - Windows Installation Guide

Simple installation guide for Windows 10 and Windows 11 users.

---

## Quick Install

### Step 1: Download Installer

Open PowerShell and run:

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/andyinva/bible-search-lite/main/setup_win11.py" -OutFile "setup_win11.py"
```

Or download manually from:
https://github.com/andyinva/bible-search-lite/blob/main/setup_win11.py

### Step 2: Run Installer

```powershell
python setup_win11.py
```

The installer will:
- ✅ Check Python version
- ✅ Download Bible database (~90 MB)
- ✅ Verify download integrity
- ✅ Extract and create SQLite database
- ✅ Download application files
- ✅ Install PyQt6
- ✅ Create Windows launcher

### Step 3: Run Application

Double-click:
```
run_bible_search.bat
```

Or run from PowerShell:
```powershell
python bible_search_lite.py
```

---

## Requirements

- **Python 3.7 or higher** - Download from https://www.python.org/downloads/
- **Internet connection** - For downloading database (one-time)
- **~500 MB disk space** - For database and application

---

## Troubleshooting

### Python Not Found

**Error:** `python: command not found`

**Solution:** Install Python from https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation

### Download Fails

**Error:** `Failed to download database`

**Solutions:**
1. Check internet connection
2. Make sure GitHub Release v1.0 exists
3. Try downloading manually from GitHub Releases

### PyQt6 Installation Fails

**Error:** `Failed to install PyQt6`

**Solution:**
```powershell
pip install PyQt6
```

If that fails, try:
```powershell
python -m pip install --upgrade pip
python -m pip install PyQt6
```

### Application Won't Start

**Error:** `ModuleNotFoundError: No module named 'PyQt6'`

**Solution:** Install PyQt6 manually (see above)

---

## Alternative: WSL2

If you prefer a Linux environment on Windows:

### Install WSL2

1. Open PowerShell as Administrator
2. Run:
   ```powershell
   wsl --install
   ```
3. Restart computer
4. Open Ubuntu from Start Menu
5. Run Linux installer:
   ```bash
   python3 setup.py
   ```

WSL2 provides a full Linux environment and works great for development!

---

## Features

See [README.md](README.md) for full feature list including:
- 44 Bible translations
- Advanced search operators (wildcards, proximity, boolean)
- Multi-window interface
- Subject management with notes
- Export to multiple formats

---

## Support

- **Issues**: https://github.com/andyinva/bible-search-lite/issues
- **Documentation**: See README.md and SEARCH_OPERATORS.md
- **Discussions**: https://github.com/andyinva/bible-search-lite/discussions

---

**Enjoy studying the Word! 📖**
