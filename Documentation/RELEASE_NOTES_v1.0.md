# Bible Search Lite v1.0 - Initial Release

## 🎉 Welcome to Bible Search Lite!

A powerful, feature-rich Bible search application with advanced search operators, 44 Bible translations, and an intuitive multi-window interface.

---

## ✨ Key Features

### Advanced Search Operators
- **`*` and `%`** - Wildcard matching for word variations (e.g., `love*` finds love, loved, loving)
- **`&`** - Word placeholder for exact patterns (e.g., `who & sent` finds "who had sent")
- **`>`** - Ordered words operator (e.g., `love > God` ensures order)
- **`~N`** - Proximity search (e.g., `love ~4 God` finds words within 4 words of each other)
- **`AND/OR`** - Boolean operators for complex queries
- **`" "`** - Exact phrase matching

### 44 Bible Translations
Including KJV (1611), NIV, ESV, NASB, and many historical translations from 1382-2023, with publication dates shown.

### Powerful Interface
- **5 Windows**: Message, Search Results, Reading, Subject Verses, Subject Comments
- **Multi-translation search** - Search across multiple Bible versions simultaneously
- **Context loading** - Click a verse to see surrounding context
- **Subject management** - Organize verses by topic with notes
- **Export features** - Export to text, markdown, or formatted documents
- **Smart filtering** - Filter results by book, testament, or custom groups

### Search Enhancements
- **Book filters** - Search within specific books or groups (Pentateuch, Gospels, Prophets, etc.)
- **Word frequency filter** - See which word variations appear in results
- **Case-sensitive search** - Optional exact matching
- **Unique verse mode** - Show each verse only once across translations
- **Search history** - Quick access to recent successful searches

---

## 📥 Installation

### One-Command Install

```bash
curl -O https://raw.githubusercontent.com/andyinva/bible-search-lite/main/setup.py
python3 setup.py
```

The installer will:
- ✅ Download the Bible database (~150MB compressed)
- ✅ Verify download integrity
- ✅ Set up SQLite database with all 44 translations
- ✅ Download all application files
- ✅ Install Python dependencies

### Requirements
- Python 3.7 or higher
- SQLite3
- PyQt6 (installed automatically)

### Running
```bash
./run_bible_search.sh
```

Or:
```bash
python3 bible_search_lite.py
```

---

## 📚 Database Information

**File**: `bible_data.sql.gz`

- **Compressed size**: ~150 MB
- **Uncompressed**: ~1.2 GB SQL dump
- **Final database**: 453 MB SQLite
- **Translations**: 44 complete Bible versions
- **Verses**: ~31,000 verses per translation
- **Total records**: 1.3+ million verses
- **Verified**: SHA256 checksum included

---

## 🔍 Search Examples

### Basic Searches
- `love` - Find all verses containing "love"
- `"in the beginning"` - Exact phrase
- `faith AND works` - Both words present

### Advanced Searches
- `love*` - love, loved, loving, lover, etc.
- `believ%` - believe, believed, believer, believing
- `who & sent` - "who had sent", "who hath sent"
- `love > neighbour` - "love" appears before "neighbour"
- `love ~4 God` - "love" and "God" within 4 words

### Filtered Searches
- Search only in Gospels
- Search only in Old Testament
- Search across all translations simultaneously

---

## 📖 Documentation

- **README.md** - Comprehensive user guide
- **SEARCH_OPERATORS.md** - Complete search operator reference
- **INSTALLATION.md** - Detailed installation instructions
- **DISTRIBUTION_GUIDE.md** - Technical documentation

---

## 🛠️ Technical Details

### Architecture
- **Language**: Python 3.7+
- **GUI Framework**: PyQt6
- **Database**: SQLite 3
- **Platform**: Linux, macOS, Windows (via WSL)

### Components
- `bible_search_lite.py` - Main application
- `bible_search.py` - Search engine
- `bible_search_service.py` - Database service
- `subject_manager.py` - Subject/topic management
- `bible_search_ui/` - UI components (widgets, dialogs, controllers)

### Database Schema
- `translations` - Bible version metadata
- `verses` - All Bible verses (1.3M+ records)
- `cross_references` - Verse cross-references
- `subjects` - User-created topics
- `subject_verses` - Verses linked to subjects

---

## 🚀 What's New in v1.0

This is the initial release with:
- ✅ 44 Bible translations with publication dates
- ✅ Advanced search operators (%, &, >, ~N)
- ✅ Multi-window interface
- ✅ Subject management system
- ✅ Export functionality
- ✅ Smart search history (only saves successful searches)
- ✅ Book group filters
- ✅ Professional one-command installer
- ✅ Cross-platform support

---

## 📝 License

**MIT License**

Copyright (c) 2026 Andrew Hopkins

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**In simple terms:**
- ✅ Free to use for any purpose (personal, commercial, ministry)
- ✅ Free to modify and distribute
- ✅ Free to include in other projects
- ✅ No warranty or liability
- ℹ️ Just keep the copyright notice

---

## 🙏 Acknowledgments

Bible translations are from public domain sources and various modern translations with appropriate permissions.

Special thanks to the open-source community for tools and libraries that made this possible.

---

## 🐛 Known Issues

- Cursor may disappear on some WSL2/X11 configurations (workaround: use native Linux or Windows)
- First search may be slower (database warming up)

---

## 📞 Support

- **Documentation**: See README.md and INSTALLATION.md
- **Issues**: https://github.com/andyinva/bible-search-lite/issues
- **Discussions**: https://github.com/andyinva/bible-search-lite/discussions

---

## 🎯 Quick Start Guide

1. **Install**: `python3 setup.py`
2. **Run**: `./run_bible_search.sh`
3. **Search**: Type "love" and click Search
4. **Click a verse**: See context in Reading Window
5. **Explore**: Try advanced operators like `love ~4 God`
6. **Create subjects**: Organize verses by topic
7. **Export**: Share your findings

---

**Enjoy studying the Word! 📖✨**

*Bible Search Lite v1.0 - January 2026*
