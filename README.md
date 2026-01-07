# Bible Search Lite

**Version**: 1.0
**Release Date**: January 2026
**License**: MIT

A powerful, feature-rich Bible search application with advanced search operators, 44 Bible translations, and an intuitive multi-window interface.

---

## Quick Start

### Installation

```bash
curl -O https://raw.githubusercontent.com/andyinva/bible-search-lite/main/setup.py
python3 setup.py
```

### Running

```bash
./run_bible_search.sh
```

Or:

```bash
python3 bible_search_lite.py
```

---

## Features

### Advanced Search Operators
- **`*` and `%`** - Wildcard matching (e.g., `love*` finds love, loved, loving)
- **`&`** - Word placeholder (e.g., `who & sent` finds "who had sent")
- **`>`** - Ordered words (e.g., `love > God` ensures order)
- **`~N`** - Proximity search (e.g., `love ~4 God` finds words within 4 words)
- **`AND/OR`** - Boolean operators
- **`" "`** - Exact phrase matching

See [SEARCH_OPERATORS.md](SEARCH_OPERATORS.md) for complete documentation.

### 44 Bible Translations
Including KJV (1611), NIV, ESV, NASB, and many historical translations from 1382-2023, with publication dates shown.

### Multi-Window Interface
- **Window 1: Message** - Status and controls
- **Window 2: Search Results** - Your search findings
- **Window 3: Reading Window** - Context and verse navigation
- **Window 4: Subject Verses** - Organize verses by topic
- **Window 5: Subject Comments** - Add rich-text notes

### Smart Features
- **Multi-translation search** - Search across multiple versions simultaneously
- **Context loading** - Click a verse to see surrounding verses
- **Subject management** - Organize verses with notes
- **Export** - Export to text, markdown, or formatted documents
- **Book filters** - Search specific books or groups
- **Search history** - Quick access to successful searches

---

## Search Examples

### Basic
```
love                    - Find all verses with "love"
"in the beginning"      - Exact phrase
faith AND works         - Both words present
```

### Advanced
```
love*                   - love, loved, loving, lover
believ%                 - believe, believed, believer
who & sent              - "who had sent", "who hath sent"
love > neighbour        - "love" before "neighbour"
love ~4 God             - "love" and "God" within 4 words
```

---

## Requirements

- Python 3.7 or higher
- SQLite3 (auto-installed on Linux/macOS)
- PyQt6 (installed automatically)
- **Windows users**: WSL2 recommended (see [INSTALLATION.md](INSTALLATION.md))

---

## Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation guide
- **[SEARCH_OPERATORS.md](SEARCH_OPERATORS.md)** - Complete search reference
- **[DISTRIBUTION_GUIDE.md](DISTRIBUTION_GUIDE.md)** - Technical documentation

---

## Database

- **44 Bible translations**
- **~31,000 verses per translation**
- **1.3+ million total verses**
- **453 MB SQLite database**
- **Compressed download: ~90 MB**

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Andrew Hopkins

Free to use for any purpose (personal, commercial, ministry). Free to modify and distribute.

---

## Support

- **Issues**: https://github.com/andyinva/bible-search-lite/issues
- **Discussions**: https://github.com/andyinva/bible-search-lite/discussions

---

**Enjoy studying the Word! 📖**
