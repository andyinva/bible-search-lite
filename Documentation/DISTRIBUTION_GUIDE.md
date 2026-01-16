# Bible Search Lite - Distribution System

## Overview

I've created a complete two-app distribution system for Bible Search Lite:

### 📤 App 1: `export_bible_data.py` (Developer Tool)
**Purpose**: Export the database for distribution
**Who uses it**: You (the developer)
**What it does**:
- Exports SQLite database to SQL dump
- Compresses with gzip (-9 for maximum compression)
- Generates SHA256 checksums for verification
- Creates files ready to upload to GitHub Releases

### 📥 App 2: `setup.py` (End User Installer)
**Purpose**: One-command installation
**Who uses it**: End users
**What it does**:
- Downloads compressed database from GitHub Releases
- Verifies download integrity with checksums
- Decompresses and imports into SQLite
- Downloads all application files
- Installs Python dependencies
- Creates complete working installation

---

## Quick Start for Developers

### 1. Export Database

```bash
python3 export_bible_data.py
```

Output:
```
data/bible_data.sql.gz    (~150 MB)
data/checksums.txt
```

### 2. Create GitHub Release

1. Go to: https://github.com/andyinva/bible-search-lite/releases
2. Click "Draft a new release"
3. Tag: `v1.0` (or your version)
4. Upload:
   - `data/bible_data.sql.gz`
   - `data/checksums.txt`
5. Publish

### 3. Users Install With

```bash
python3 setup.py
```

Done! They have a complete installation.

---

## Quick Start for End Users

### Installation (One Command)

```bash
curl -O https://raw.githubusercontent.com/andyinva/bible-search-lite/main/setup.py
python3 setup.py
```

The installer does everything automatically:
- ✅ Downloads Bible database
- ✅ Verifies integrity
- ✅ Sets up SQLite
- ✅ Downloads app files
- ✅ Installs dependencies

### Running

```bash
./run_bible_search.sh
```

Or:

```bash
python3 bible_search_lite.py
```

---

## Technical Details

### Database Size Breakdown

| Stage | Size | Format |
|-------|------|--------|
| Original | 453 MB | SQLite binary |
| SQL Dump | ~1.2 GB | Uncompressed SQL |
| Compressed | ~150 MB | gzip -9 |
| Download | ~150 MB | What users download |
| Final DB | 453 MB | SQLite after import |

### Why GitHub Releases?

- ✅ Designed for large binary files (2GB limit)
- ✅ Free CDN distribution
- ✅ Automatic checksums
- ✅ Version tracking
- ✅ Download statistics
- ❌ Regular repo has 100MB file limit

### Export Process Flow

```
1. export_bible_data.py runs
2. sqlite3 bibles.db .dump > bible_data.sql
3. gzip -9 bible_data.sql (maximum compression)
4. Calculate SHA256 checksum
5. Create checksums.txt
6. Files ready in data/ directory
7. Upload to GitHub Releases
```

### Install Process Flow

```
1. setup.py downloads checksums.txt
2. Downloads bible_data.sql.gz from Release
3. Verifies SHA256 checksum
4. gunzip bible_data.sql.gz
5. sqlite3 bibles.db < bible_data.sql
6. Downloads app files from main branch
7. pip install PyQt6
8. Complete!
```

---

## Files Created

### New Files

```
export_bible_data.py        Developer: Export database
setup.py                    End user: Install everything
INSTALLATION.md             Installation instructions
DISTRIBUTION_GUIDE.md       This file
```

### Generated Files (by export script)

```
data/
├── bible_data.sql.gz      Upload to GitHub Releases
└── checksums.txt          Upload to GitHub Releases
```

### Created by Installer

```
database/
├── bibles.db              453 MB - Bible translations
└── subjects.db            User data (empty template)
temp/                      Temporary files (auto-cleaned)
```

---

## Workflow

### For Each New Release

1. **Make your changes** to the application
2. **Test thoroughly**
3. **Export database**:
   ```bash
   python3 export_bible_data.py
   ```
4. **Create GitHub Release** (v1.0, v1.1, etc.)
5. **Upload** `data/bible_data.sql.gz` and `data/checksums.txt`
6. **Update** `RELEASE_VERSION` in `setup.py`
7. **Commit and push** setup.py change
8. **Announce** to users

Users then run:
```bash
python3 setup.py
```

---

## Advantages of This Approach

### For Users
- ✅ One-command installation
- ✅ Automatic dependency installation
- ✅ Download verification (checksums)
- ✅ Progress indicators
- ✅ Clear error messages
- ✅ No manual steps

### For You (Developer)
- ✅ Simple export process
- ✅ No repo bloat (files in Releases)
- ✅ Version control for database
- ✅ Easy to update
- ✅ Automatic distribution via GitHub CDN
- ✅ Download statistics

### Technical
- ✅ Preserves schema, indexes, data
- ✅ Cross-platform (Linux, macOS, WSL)
- ✅ Verifiable downloads
- ✅ Efficient compression
- ✅ Standard tools (sqlite3, gzip)

---

## Future Enhancements

Possible improvements:

1. **Progress bar** - Add `tqdm` for better download progress
2. **Resume downloads** - Support interrupted downloads
3. **Mirror support** - Multiple download sources
4. **Incremental updates** - Only download changes
5. **Auto-updater** - Check for new versions
6. **GUI installer** - PyQt6-based installer
7. **Windows .exe** - PyInstaller bundle
8. **Snap/Flatpak** - Linux app store distribution

---

## Comparison to Other Approaches

### Option A: Store DB in Repo ❌
- Pros: Simple
- Cons: 453MB exceeds 100MB limit, bloats repo history

### Option B: Git LFS ❌
- Pros: Handles large files
- Cons: Costs money, complex, bandwidth limits

### Option C: External hosting ❌
- Pros: No GitHub limits
- Cons: Costs money, maintenance, reliability

### Option D: GitHub Releases ✅ **CHOSEN**
- Pros: Free, CDN, version tracking, reliable
- Cons: Manual release process (but scripted!)

---

## Testing

### Test Export

```bash
python3 export_bible_data.py
ls -lh data/
```

Expected:
- `bible_data.sql.gz` (~150 MB)
- `checksums.txt` (small text file)

### Test Install (In Clean Directory)

```bash
mkdir test_install
cd test_install
curl -O https://raw.githubusercontent.com/andyinva/bible-search-lite/main/setup.py
python3 setup.py
```

Expected:
- Downloads complete
- Database created
- App files downloaded
- Dependencies installed
- Ready to run

---

## Support

If users have issues:

1. Check INSTALLATION.md
2. Verify GitHub Release exists
3. Test checksums manually
4. Check internet connection
5. Verify required tools installed

---

## Summary

You now have a professional distribution system:

- **export_bible_data.py** - One command to export
- **setup.py** - One command for users to install
- **INSTALLATION.md** - Complete instructions
- **GitHub Releases** - Free, reliable distribution

This is the same approach used by many professional open-source projects!
