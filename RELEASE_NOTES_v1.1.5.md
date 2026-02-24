# Release Notes - Bible Search Lite v1.1.5

**Release Date:** February 24, 2026

## What's New

### Enhanced Wildcard Search
- **Improved `?` wildcard matching**: Now correctly handles possessive forms (e.g., `"father'?"` matches "father's")
- Single character wildcard now matches letters and apostrophes for better accuracy

### Filter Dialog Improvements
- **Message retention fix**: Filter button no longer clears the message window
- Message history is preserved when using cached word counts

### Documentation Updates
- **Enhanced SEARCH_OPERATORS.md**:
  - Added clear explanation of `?` vs `*` wildcard behavior
  - New "Common Issues and Solutions" troubleshooting section
  - Added "Key Point" column to Quick Reference Table
  - Better examples showing exact length requirements for `?` wildcard

## Bug Fixes

- Fixed: Filter button was clearing "Analyzing word variations..." message unnecessarily
- Fixed: `?` wildcard pattern now includes apostrophe characters for possessive matching

## Previous Releases (since v1.1.4)

- **Create button enhancement**: Smart state management for creating subjects
- **Release wizard fix**: Correctly updates VERSION in bible_search_lite.py
- **Windows launcher improvement**: Works from any location (Desktop, Start Menu, etc.)

## Database

- 39 Bible translations
- 32,584 unique verses
- 980,606 verse texts
- Optimized with composite indexes

## Installation

### New Installation
```bash
# Download and run setup
python3 -c "import urllib.request; urllib.request.urlretrieve('https://raw.githubusercontent.com/andyinva/bible-search-lite/main/setup.py', 'setup.py')" && python3 setup.py
```

### Windows Installation
```powershell
# Download and run Windows setup
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/andyinva/bible-search-lite/main/setup_win11.py" -OutFile "setup_win11.py"; python setup_win11.py
```

### Update Existing Installation
Use the built-in updater: **File > Check for Updates**

## Requirements

- Python 3.7+
- PyQt6
- Internet connection (for installation)

## Full Changelog

See all commits at: https://github.com/andyinva/bible-search-lite/compare/v1.1.4...v1.1.5

---

🔗 **Download**: https://github.com/andyinva/bible-search-lite/releases/tag/v1.1.5
