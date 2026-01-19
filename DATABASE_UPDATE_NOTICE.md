# Database Update Notice

## Important: Database Now Tracked in Git

**Date:** January 18, 2026
**Affects:** Users who installed before v1.1.0

---

## What Changed

The Bible database (`database/bibles.db`) is **NOT** in the git repository because it's 406 MB (GitHub limit is 100 MB).

Previously:
- Users kept whatever database version they had
- Updates to the database weren't distributed
- Some users had 45 translations (old), others had 37 (new)

**Now:** The database must be downloaded separately from GitHub Releases.

---

## Current Database: 37 Translations

The correct database contains **37 translations** with complete publication dates.

To check your current database:
```bash
sqlite3 database/bibles.db "SELECT COUNT(*) FROM translations;"
```

Expected result: **37**

---

## Download the Correct Database

The 37-translation database (406 MB) is available as a release asset on GitHub.

### Quick Download:

**Linux/WSL/Mac:**
```bash
cd bible-search-lite/database
wget https://github.com/andyinva/bible-search-lite/releases/download/v1.1.0/bibles.db
```

**Windows PowerShell:**
```powershell
cd bible-search-lite\database
Invoke-WebRequest -Uri "https://github.com/andyinva/bible-search-lite/releases/download/v1.1.0/bibles.db" -OutFile "bibles.db"
```

### Manual Download:
1. Go to: https://github.com/andyinva/bible-search-lite/releases/tag/v1.1.0
2. Download `bibles.db` (406 MB)
3. Place it in the `database/` directory

See `database/DOWNLOAD_DATABASE.md` for complete instructions.

---

## Verify You Have the Correct Database

After updating, verify you have the correct version:

```bash
sqlite3 database/bibles.db "SELECT COUNT(*) as total,
    (SELECT abbreviation FROM translations ORDER BY id LIMIT 1) as first,
    (SELECT abbreviation FROM translations ORDER BY id DESC LIMIT 1) as last
FROM translations;"
```

**Expected output:**
```
37|KJV|ACV
```

Or check translations list:
```bash
sqlite3 database/bibles.db "SELECT abbreviation FROM translations ORDER BY abbreviation;"
```

**Should show 37 translations:**
- ACV, AND, ASV, BBE, BIS, BSB, BST, COV, CPD, DBT, DRC, DRB, ERV, GEN, GN2, HAW, JPS, JUB, KJV, LEB, LIT, MKJ, NET, NHE, NHJ, NHM, NOY, OEB, OEC, ROT, TWE, TYD, TYN, WEB, WNT, WYC, YLT

---

## Why 37 Instead of 45?

The database was cleaned up to:
- Remove duplicate or redundant translations
- Focus on historically significant and widely-used translations
- Improve quality over quantity
- Add complete publication dates for all translations

All 37 translations now have:
- Proper names with publication dates
- Clean formatting
- Historical accuracy
- Full coverage of Old and New Testament

---

## User Data Safety

**Don't worry about losing your data!**

The following user files are still ignored by git and won't be affected:
- `bible_search_lite_config.json` - Your settings and search history
- `database/subjects.db` - Your subject collections
- `database/user_data.db` - Any user-specific data

Only the Bible translations database (`bibles.db`) is now tracked.

---

## For New Users

If you're cloning the repository for the first time, you'll automatically get the correct 37-translation database. No action needed!

---

## Questions?

If you have issues updating the database:
1. Check the troubleshooting steps above
2. Make sure you don't have the app running (close it first)
3. Check file permissions on the database directory
4. Try a fresh clone if problems persist

---

**This change was made in v1.1.0 to ensure all users have the correct, up-to-date Bible translations database.**
