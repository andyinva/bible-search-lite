# Bible Search Lite - Windows Quick Start

## Installation (3 Simple Steps)

### Step 1: Download Installer

Open PowerShell and run:
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/andyinva/bible-search-lite/main/setup_win11.py" -OutFile "setup_win11.py"
```

### Step 2: Run Installer

```powershell
python setup_win11.py
```

This will:
- Download the Bible database from GitHub Release v1.0 (~90 MB)
- Verify the download with checksums
- Extract and create the SQLite database
- Download all application files
- Install PyQt6
- Create `run_bible_search.bat` launcher

### Step 3: Launch Application

Double-click:
```
run_bible_search.bat
```

---

## Requirements

- **Python 3.7+** (with "Add Python to PATH" enabled)
- **Internet connection** (for one-time download)
- **~500 MB disk space**

---

## What Gets Installed

```
bible-search-lite/
├── database/
│   ├── bibles.db          (453 MB - 44 translations)
│   └── subjects.db        (User notes and subjects)
├── bible_search_lite.py   (Main application)
├── bible_search.py        (Search engine)
├── bible_search_service.py
├── subject_manager.py
├── bible_search_ui/       (UI components)
├── run_bible_search.bat   (Windows launcher)
└── README.md              (Full documentation)
```

---

## Troubleshooting

**Python not found?**
- Download from https://www.python.org/downloads/
- During install, check "Add Python to PATH"

**Download fails?**
- Check internet connection
- Make sure you can access github.com

**PyQt6 won't install?**
```powershell
python -m pip install --upgrade pip
python -m pip install PyQt6
```

---

**Enjoy! 📖**
