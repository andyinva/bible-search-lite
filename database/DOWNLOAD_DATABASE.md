# Bible Search Lite - Database Download Instructions

**The Bible database file is too large for GitHub (about 397 MB)**

This file contains 33 Bible translations and must be downloaded separately.

The published database holds only translations that may be passed on.
Six translations still under copyright (JUB, LEB, NET, LIT, MKJ, BBE) are
left out of it.  The developer's own copy keeps them; the public copy is
made from it with `python3 make_public_database.py`.

---

## Quick Download

### For Linux/WSL/Mac:
```bash
cd database
wget https://github.com/andyinva/bible-search-lite/releases/download/v1.1.6/bibles.db
# OR
curl -L -o bibles.db https://github.com/andyinva/bible-search-lite/releases/download/v1.1.6/bibles.db
```

### For Windows PowerShell:
```powershell
cd database
Invoke-WebRequest -Uri "https://github.com/andyinva/bible-search-lite/releases/download/v1.1.6/bibles.db" -OutFile "bibles.db"
```

---

## Manual Download

1. Go to: https://github.com/andyinva/bible-search-lite/releases/tag/v1.1.6
2. Download `bibles.db` (about 397 MB)
3. Place it in the `database/` directory

---

## Verify Database

After downloading, verify it's correct:

```bash
sqlite3 bibles.db "SELECT COUNT(*) FROM translations;"
```

**Expected:** 33

---

## Database Contents

- **33 Bible Translations** with complete publication dates
- **All books** of the Old and New Testament
- **Cross-references** and verse data
- **~397 MB** SQLite database

### Included Translations:
ACV, AND, ASV, BIS, BSB, BST, COV, CPD, DBT, DRB, DRC, EDG, ERV, GEN, GN2, HAW, JPS, KJV, NHE, NHJ, NHM, NOY, OEB, OEC, ROT, SLT, TWE, TYD, TYN, WEB, WNT, WYC, YLT

---

## Troubleshooting

**"File not found"**
- Make sure you're in the `database/` directory
- Check the URL is correct for the latest release

**"Database is locked"**
- Close Bible Search Lite before downloading
- Make sure no other program is using the database

**"Wrong number of translations"**
- Delete the old database completely
- Re-download from the link above
- Verify with the SQL query above

---

## Alternative: Copy from Working Installation

If you have access to another working installation:

```bash
cp /path/to/working/bible-search-lite/database/bibles.db ./database/
```

---

**Note:** This database will be included in future releases as a separate download due to GitHub's 100 MB file size limit.
