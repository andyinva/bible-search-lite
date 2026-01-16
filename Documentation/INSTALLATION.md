# Bible Search Lite - Installation Guide

## For End Users: Quick Install

### One-Command Installation

```bash
python3 setup.py
```

That's it! The installer will:
1. Download the Bible database (~150MB compressed)
2. Verify the download integrity
3. Set up the SQLite database
4. Download all application files
5. Install Python dependencies

### Requirements

- Python 3.7 or higher
- Internet connection
- `sqlite3` command-line tool
- `gzip` utility

On Ubuntu/Debian:
```bash
sudo apt-get install python3 sqlite3 gzip python3-pip
```

On macOS:
```bash
brew install python sqlite3
```

### Running Bible Search Lite

After installation completes:

```bash
./run_bible_search.sh
```

Or:

```bash
python3 bible_search_lite.py
```

---

## For Developers: Creating a Release

### Step 1: Export the Database

Run the exporter script:

```bash
python3 export_bible_data.py
```

This creates:
- `data/bible_data.sql.gz` - Compressed database (~150MB)
- `data/checksums.txt` - SHA256 checksums

### Step 2: Create GitHub Release

1. Go to: https://github.com/andyinva/bible-search-lite/releases
2. Click "Draft a new release"
3. Create a new tag (e.g., `v1.0`)
4. Upload these files to the release:
   - `data/bible_data.sql.gz`
   - `data/checksums.txt`
5. Publish the release

### Step 3: Update setup.py

Edit `setup.py` and update the version:

```python
RELEASE_VERSION = "v1.0"  # Match your release tag
```

Commit and push the change.

### Step 4: Test the Installer

In a clean directory:

```bash
curl -O https://raw.githubusercontent.com/andyinva/bible-search-lite/main/setup.py
python3 setup.py
```

---

## Architecture

### Export Process

```
bibles.db (453 MB)
    ↓ sqlite3 .dump
bible_data.sql (1.2 GB)
    ↓ gzip -9
bible_data.sql.gz (~150 MB)
    ↓ upload to GitHub Releases
Distribution ready!
```

### Install Process

```
Download bible_data.sql.gz from GitHub Releases
    ↓ verify SHA256 checksum
    ↓ gunzip
bible_data.sql
    ↓ sqlite3 < bible_data.sql
bibles.db (453 MB)
    ↓ download app files from GitHub
Complete installation!
```

---

## Files Structure

```
bible-search-lite/
├── export_bible_data.py    # Developer: Export database
├── setup.py                 # End user: Install everything
├── data/                    # Created by export script
│   ├── bible_data.sql.gz   # Upload to GitHub Releases
│   └── checksums.txt       # Upload to GitHub Releases
├── database/
│   ├── bibles.db           # Created by setup.py
│   └── subjects.db         # User data
├── bible_search_lite.py    # Main application
├── bible_search_ui/        # UI components
└── ...
```

---

## Troubleshooting

### Setup fails to download

- Check your internet connection
- Verify the GitHub Release exists: https://github.com/andyinva/bible-search-lite/releases
- Make sure `RELEASE_VERSION` in setup.py matches the release tag

### Checksum verification fails

- Re-download setup.py
- Try downloading again (file may have been corrupted)
- Verify checksums.txt was uploaded correctly to the release

### Missing sqlite3 or gzip

Install the required tools:

**Ubuntu/Debian:**
```bash
sudo apt-get install sqlite3 gzip
```

**macOS:**
```bash
brew install sqlite3
```

**Windows (WSL):**
```bash
sudo apt-get install sqlite3 gzip
```

---

## Size Information

- **Original database**: 453 MB (SQLite)
- **SQL dump**: ~1.2 GB (uncompressed)
- **Compressed**: ~150 MB (gzip -9)
- **Download time**: ~2-5 minutes on typical connection

The compressed file is small enough for GitHub Releases (2GB limit) and reasonable for users to download.

---

## Advanced: Manual Installation

If the automated installer doesn't work, you can install manually:

1. Download database:
   ```bash
   wget https://github.com/andyinva/bible-search-lite/releases/download/v1.0/bible_data.sql.gz
   ```

2. Decompress:
   ```bash
   gunzip bible_data.sql.gz
   ```

3. Create database:
   ```bash
   mkdir -p database
   sqlite3 database/bibles.db < bible_data.sql
   ```

4. Download application files from GitHub

5. Install dependencies:
   ```bash
   pip install PyQt6
   ```

6. Run:
   ```bash
   python3 bible_search_lite.py
   ```

---

## Questions?

Open an issue on GitHub: https://github.com/andyinva/bible-search-lite/issues
