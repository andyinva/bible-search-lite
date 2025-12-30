# Bible Search Lite - Comprehensive Documentation

**Version**: 3.0 (Modular Architecture)
**Last Updated**: December 29, 2025
**Location**: `/home/ajhinva/projects/bible-search-lite-test2/`

---

## Table of Contents

1. [Application Overview](#application-overview)
2. [Architecture](#architecture)
3. [User Interface](#user-interface)
4. [Features](#features)
5. [File Structure](#file-structure)
6. [Database Schema](#database-schema)
7. [Configuration](#configuration)
8. [Development Guide](#development-guide)
9. [Bug Fixes and Known Issues](#bug-fixes-and-known-issues)
10. [Future Enhancements](#future-enhancements)

---

## Application Overview

### Purpose
Bible Search Lite is a desktop application for searching, studying, and organizing Bible verses across multiple translations. It provides powerful search capabilities, context viewing, and personal verse collection management with notes.

### Key Capabilities
- **Multi-translation search** - Search across KJV, NIV, ESV, NASB, and more
- **Context viewing** - See surrounding verses for any search result
- **Personal collections** - Organize verses into subjects with rich-text comments
- **Flexible export** - Export to CSV, RTF, or printer
- **Smart filtering** - Filter results by book, chapter, word occurrence
- **Persistent settings** - Window sizes, fonts, and preferences saved automatically

### Target Users
- Bible students and researchers
- Pastors preparing sermons
- Sunday school teachers
- Anyone studying scripture

---

## Architecture

### Design Pattern
Bible Search Lite uses a **modular architecture** with clear separation of concerns:

```
Main Application (bible_search_lite.py)
├── UI Layer (PyQt6 widgets)
├── Search Layer (SearchController)
├── Modular Features
│   ├── SubjectManager (Windows 4 & 5 coordinator)
│   ├── SubjectVerseManager (Window 4 logic)
│   ├── SubjectCommentManager (Window 5 logic)
│   └── ExportDialog (Export feature)
└── Configuration (ConfigManager)
```

### Core Components

#### 1. **Main Application** (`bible_search_lite.py`)
- **Purpose**: Main window and application orchestration
- **Responsibilities**:
  - Window management (Windows 1-3)
  - Search coordination
  - User preferences
  - Signal/slot connections
- **Key Classes**:
  - `BibleSearchProgram` - Main application window
  - `SelectionManager` - Manages verse selection across windows

#### 2. **Search Layer** (`SearchController`)
- **Purpose**: Bible search logic
- **Location**: `bible_search_ui/controllers/search_controller.py`
- **Responsibilities**:
  - Query parsing (AND/OR operators, wildcards)
  - Database queries
  - Result formatting
  - Unique verse deduplication

#### 3. **Subject Management** (Modular)
Files: `subject_manager.py`, `subject_verse_manager.py`, `subject_comment_manager.py`

**SubjectManager** - Container/orchestrator
- Manages Windows 4 & 5 as a unit
- Handles show/hide/toggle
- Coordinates database connection
- Saves visibility preference

**SubjectVerseManager** - Window 4 (Subject Verses)
- Subject creation and management
- Verse acquisition from Windows 2 & 3
- Verse deletion
- Subject renaming/deletion

**SubjectCommentManager** - Window 5 (Comments)
- Rich-text comment editor
- Formatting toolbar (bold, italic, underline, font size)
- HTML comment storage
- Collapsible UI (toolbar only shows when editing)

#### 4. **Export Feature** (`export_dialog.py`)
- **Purpose**: Comprehensive verse export
- **Formats**: CSV, RTF
- **Sources**: Search results, Reading window, Subject verses, Messages
- **Options**: Selected vs all, include comments, custom save location
- **Output**: File or printer

#### 5. **UI Widgets** (`bible_search_ui/ui/widgets.py`)
- `VerseItemWidget` - Individual verse display with checkbox
- `VerseListWidget` - Scrollable verse container
- `SectionWidget` - Window container with title bar and buttons

#### 6. **Configuration** (`ConfigManager`)
- **Location**: `bible_search_ui/config/config_manager.py`
- **File**: `bible_search_lite_config.json`
- **Stores**:
  - Window geometry and splitter sizes
  - Font settings
  - Checkbox states
  - Search history
  - Selected translations
  - Subject window visibility

---

## User Interface

### Window Layout

```
┌─────────────────────────────────────────────┐
│ 1. Message Window                           │
│    [Help] [Copy] [Export] [📑]              │
│    Search: "faith" | Total: 850 | Time: 0.4s│
├─────────────────────────────────────────────┤
│ 2. Search Results                           │
│    [Search] [Translations] [Filter] [Delete]│
│    ☐ John 3:16 (KJV) For God so loved...    │
│    ☐ Romans 8:28 (KJV) And we know that...  │
├─────────────────────────────────────────────┤
│ 3. Reading Window                           │
│    [Subject ▼] [Send] [References ▼]        │
│    ☐ John 3:14 (KJV) And as Moses lifted... │
│    ☐ John 3:15 (KJV) That whosoever...      │
│    ☐ John 3:16 (KJV) For God so loved...    │ ← Highlighted
│    ☐ John 3:17 (KJV) For God sent not...    │
├─────────────────────────────────────────────┤
│ 4. Subject Verses (toggleable)              │
│    [Subject ▼] [Create] [Acquire] [Delete]  │
│    ☐ John 3:16 (KJV) For God so loved...    │
├─────────────────────────────────────────────┤
│ 5. Subject Comments (toggleable)            │
│    [Add] [Edit] [Save] [Delete] [Close]     │
│    [B] [I] [U] [Font ▼]  ← Toolbar          │
│    This verse explains God's love...         │
└─────────────────────────────────────────────┘
```

### Window Functions

#### Window 1: Message Window
**Purpose**: Status messages and app controls

**Features**:
- **Help button** - Opens help menu with topics:
  - Window 2: Search Results Help
  - Window 3: Reading Window Help
  - Window 4: Subject Window Help
  - Export Feature Help
- **Copy button** - Copy checked verses from active window to clipboard
- **Export button** - Opens export dialog
- **📑 button** - Toggle Windows 4 & 5 visibility (green when visible)
- **⚙ button** - Settings (font sizes, toggle Windows 4 & 5)

**Message Format**:
```
Search: "query" | Total: 1900 | Unique: 434 | Filtered: 47 | Time: 0.45s
```
- **Search**: Exact query entered (preserves multi-word queries)
- **Total**: All matching verses across translations
- **Unique**: Deduplicated count (when "Unique Verses" checked)
- **Filtered**: Results after word filter (when filter applied)
- **Time**: Search duration in seconds

#### Window 2: Search Results
**Purpose**: Display search findings

**Controls**:
- **Search box** - Enter search terms
  - Supports: wildcards (`faith*`), AND/OR operators, phrases (`"exact match"`)
  - Dropdown shows search history
- **Translations button** - Select which Bible versions to search
- **Filter button** - Filter by:
  - Book groups (Old Testament, New Testament, specific books)
  - Word occurrence (filter results to verses containing specific words)
- **Delete button** - Delete checked verses from window
- **Clear button** - Clear all results

**Checkboxes**:
- **Case Sensitive** - Match case exactly
- **Unique Verses** - Show only one translation per verse reference
- **Abbreviate Results** - Shorten common words (e.g., "Lord" → "Ld")

**Verse Actions**:
- **Click verse** → Loads surrounding context in Window 3
- **Check box** → Select for copy/export/send to subject

#### Window 3: Reading Window
**Purpose**: Display context and manage verse organization

**Controls**:
- **Subject dropdown** - Select subject to send verses to
- **Send button** - Add checked verses to selected subject
- **References dropdown** - Navigate to cross-references

**Features**:
- Shows surrounding verses when verse clicked in Window 2
- Highlighted verse shows which one was clicked
- Checkbox selection for sending to subjects
- Clear button to empty window

#### Window 4: Subject Verses
**Purpose**: Manage verse collections

**Controls**:
- **Subject dropdown** - Select/create subject (editable)
- **Create button** - Create new subject from dropdown text
- **Acquire button** - Add checked verses from Windows 2 or 3
- **Delete button** - Delete checked verses from subject
- **Rename button** - Rename current subject
- **Delete Subject button** - Delete subject (warns about comments)
- **Clear Subject button** - Clear display without deleting

**Features**:
- Verse list shows all verses in selected subject
- Syncs with Window 3's subject dropdown when opened
- Button states update based on selections

#### Window 5: Subject Comments
**Purpose**: Add rich-text notes to verses

**Controls**:
- **Add Comment button** - Start new comment for selected verse
- **Edit button** - Edit existing comment
- **Save button** - Save comment as HTML
- **Delete button** - Delete comment
- **Close button** - Cancel editing

**Formatting Toolbar** (appears when editing):
- **B** - Bold text
- **I** - Italic text
- **U** - Underline text
- **Font Size dropdown** - Change text size

**Features**:
- Rich-text HTML editor
- Comments stored per verse in database
- Toolbar collapses when not editing

---

## Features

### 1. Search Feature

#### Search Syntax
- **Simple search**: `love` - finds "love" anywhere
- **Wildcard**: `faith*` - matches faith, faithful, faithfulness
- **AND operator**: `who AND sent` - both words must appear
- **OR operator**: `send OR sent` - either word
- **Exact phrase**: `"the Lord"` - exact phrase match
- **Complex**: `("day of the Lord" OR "day of God") AND judgment`

#### Search Options
- **Case Sensitive** - Exact case matching
- **Unique Verses** - Deduplicate across translations
- **Abbreviate Results** - Shorten display text
- **Translation Selection** - Choose which versions to search
- **Book Filter** - Limit to Old/New Testament or specific books
- **Word Filter** - Further filter results to verses containing specific words

#### Search Performance
- Average search: 0.3-0.6 seconds
- Large result sets cached for filtering
- Lazy loading for huge result sets (future)

### 2. Export Feature

#### Export Sources
1. **Search Results (Window 2)**
   - Selected verses (checked boxes)
   - All search results
2. **Reading Window (Window 3)**
   - Selected verses
   - All verses in window
3. **Subject Verses (Window 4)**
   - Selected verses from subject
   - All verses in subject
   - Option to include comments
4. **Messages Database**
   - Export message window content

#### Export Formats

**CSV (Comma Delimited)**
- Columns: Reference, Text, Comment
- UTF-8 encoding
- Header row with source and timestamp
- Best for: Excel, data analysis, importing to other tools

**RTF (Rich Text Format)**
- Bold references
- Plain verse text
- Italic comments
- Proper spacing and paragraphs
- Best for: Word, printing, sharing formatted documents

#### Export Options
- **Selection**: Selected (checked) verses vs all verses
- **Include Comments**: For subject exports
- **Save Location**:
  - Default: `downloads/` subfolder
  - Custom: Browse to any folder
  - Reset button to return to default
- **Output**:
  - File (CSV or RTF)
  - Printer (formatted document)

#### File Naming
Format: `[Source]_[Timestamp].[ext]`

Examples:
- `Search_Results_20251229_103045.csv`
- `Subject_Love_Verses_20251229_104500.rtf`
- `Reading_Window_20251229_105200.csv`

### 3. Subject Management

#### Subject Organization
- **Subjects** - Top-level collections (e.g., "Love", "Faith", "Prayer")
- **Verses** - Bible verses saved to subjects
- **Comments** - Rich-text notes attached to verses

#### Workflow
1. **Search** for verses in Window 2
2. **Click** verse to see context in Window 3
3. **Select** subject in Window 3 dropdown
4. **Check** verses you want to save
5. **Click Send** to add to subject
6. **Open** Windows 4 & 5 (📑 button) to review
7. **Add comments** to verses in Window 5
8. **Export** subject with comments when needed

#### Subject Database
- Location: `database/subjects.db`
- Tables: `subjects`, `subject_verses`, `subject_comments`
- Relationships: Foreign keys with CASCADE delete
- Comments stored as HTML

### 4. Copy Feature

#### Usage
1. Click on a window (2, 3, or 4) to activate it
2. Check boxes next to verses you want
3. Click **Copy** button
4. Paste into any application

#### Format
```
John 3:16 (KJV)
For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.

Romans 8:28 (NIV)
And we know that in all things God works for the good of those who love him, who have been called according to his purpose.
```

- Reference with translation
- Verse text
- Blank line between verses

### 5. Persistence Features

All settings automatically saved:

#### Window Settings
- Position and size
- Splitter positions (between windows)
- Windows 4 & 5 visibility state

#### User Preferences
- Selected translations
- Checkbox states (Case Sensitive, Unique Verses, Abbreviate)
- Font sizes for titles and verses
- Search history (last 50 searches)

#### Behavior
- Settings saved on exit
- Restored on startup
- Config file: `bible_search_lite_config.json`

---

## File Structure

### Core Application Files
```
bible-search-lite-test2/
├── bible_search_lite.py          # Main application (3200 lines)
├── bible_search.py                # Search module (1000 lines)
├── bible_search_service.py        # Service layer (350 lines)
├── export_dialog.py               # Export feature (600 lines)
├── subject_manager.py             # Subject coordinator (200 lines)
├── subject_verse_manager.py       # Window 4 logic (550 lines)
├── subject_comment_manager.py     # Window 5 logic (400 lines)
└── run_bible_search.sh            # Launch script
```

### UI Components
```
bible_search_ui/
├── __init__.py
├── config/
│   ├── __init__.py
│   └── config_manager.py          # Configuration management
├── controllers/
│   ├── __init__.py
│   └── search_controller.py       # Search logic
└── ui/
    ├── __init__.py
    ├── dialogs.py                 # Translation/Filter/Font dialogs
    └── widgets.py                 # VerseItemWidget, VerseListWidget
```

### Database Files
```
database/
├── bibles.db                      # Bible text (all translations) - 453MB
└── subjects.db                    # User's subject collections (Windows 4 & 5)
```

### Configuration
```
bible_search_lite_config.json     # User preferences (auto-generated)
```

### Documentation
```
Documentation/
├── COMPREHENSIVE_DOCUMENTATION.md  # This file
├── EXPORT_FEATURE.md              # Export feature details
├── SEARCH_STATUS_MESSAGE.md       # Search message format
├── SUBJECT_SYNC_FEATURE.md        # Subject sync details
├── IMPLEMENTATION_STATUS.md       # Development status
└── [other historical docs]
```

### Utilities
```
Utilities/
├── init_database.py               # Bible database setup
├── init_subjects_database.py      # Subjects database setup
├── check_database.py              # Database verification
├── patch_database.py              # Database migrations
└── [test files and dev utilities]
```

---

## Database Schema

### Bible Database (`bibles.db`)

#### Table: `bible_verses`
Stores all Bible verses across translations.

```sql
CREATE TABLE bible_verses (
    id INTEGER PRIMARY KEY,
    translation TEXT,       -- KJV, NIV, ESV, etc.
    book TEXT,              -- Genesis, Exodus, etc.
    book_abbrev TEXT,       -- Gen, Exod, etc.
    chapter INTEGER,
    verse INTEGER,
    text TEXT,              -- Verse content
    -- Indexes for fast searching
    INDEX idx_translation (translation),
    INDEX idx_book (book),
    INDEX idx_chapter (book, chapter)
);
```

**Translations Available**:
- KJV (King James Version)
- NIV (New International Version)
- ESV (English Standard Version)
- NASB (New American Standard Bible)
- [others as added]

### Subjects Database (`database/subjects.db`)

#### Table: `subjects`
Stores subject collections.

```sql
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Table: `subject_verses`
Stores verses associated with subjects.

```sql
CREATE TABLE subject_verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    text TEXT NOT NULL,
    translation TEXT NOT NULL,
    order_index INTEGER DEFAULT 0,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE INDEX idx_subject_verses_subject ON subject_verses(subject_id);
```

#### Table: `subject_comments`
Stores rich-text comments for verses.

```sql
CREATE TABLE subject_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    verse_id INTEGER NOT NULL,
    comment TEXT,               -- HTML formatted
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (verse_id) REFERENCES subject_verses(id) ON DELETE CASCADE,
    UNIQUE(subject_id, verse_id)
);
```

**Design Notes**:
- CASCADE delete ensures comments are deleted when subject/verse deleted
- UNIQUE constraint ensures one comment per verse per subject
- HTML storage allows rich formatting
- Timestamps track creation and modification

---

## Configuration

### Config File: `bible_search_lite_config.json`

```json
{
  "window_geometry": {
    "x": -3,
    "y": -30,
    "width": 1063,
    "height": 687
  },
  "splitter_sizes": [
    93,     // Window 1 height
    233,    // Window 2 height
    349     // Window 3 height
  ],
  "subject_splitter_sizes": [
    311,    // Window 4 height
    207     // Window 5 height
  ],
  "selected_translations": ["KJV"],
  "checkboxes": {
    "case_sensitive": false,
    "unique_verse": true,
    "abbreviate_results": false
  },
  "font_settings": {
    "title_font_size": 1,    // Index into font sizes array
    "verse_font_size": 2
  },
  "search_history": [
    "faith*",
    "who AND sent",
    "love"
  ],
  "ShowSubjectFeatures": false  // Windows 4 & 5 visibility
}
```

### Font Sizes

**Title Font Sizes**:
```python
[8.0, 9.0, 10.0, 11.0, 12.0, 14.0, 16.0]
```

**Verse Font Sizes**:
```python
[8.0, 9.0, 10.0, 11.0, 12.0, 14.0, 16.0, 18.0]
```

Accessed via index in config (0-6 for titles, 0-7 for verses).

---

## Development Guide

### Adding a New Feature

#### 1. Determine Architecture
Ask: Is this a major feature that should be modular?

**Modular** (separate file):
- Self-contained functionality
- Multiple methods/UI elements
- Could be reused or toggled
- Example: Export, Subject Management

**Integrated** (in main file):
- Simple enhancement to existing window
- Tightly coupled to existing code
- Few methods
- Example: New button in Window 2

#### 2. Create Module (if modular)

**Template**:
```python
"""
[Feature Name] - [Purpose]

[Description]
"""

from PyQt6.QtWidgets import (...)
from PyQt6.QtCore import Qt

class FeatureManager:
    """[Description]"""

    def __init__(self, parent_app):
        """Initialize feature manager"""
        self.parent_app = parent_app
        # Initialize state

    def create_ui(self):
        """Build UI for this feature"""
        # Create widgets
        # Return section widget
        pass

    def cleanup(self):
        """Clean up resources"""
        pass
```

#### 3. Integrate with Main Application

**In `bible_search_lite.py`**:
```python
# Import
from feature_manager import FeatureManager

# In __init__
self.feature_manager = None

# In setup_ui
self.feature_manager = FeatureManager(self)
feature_widget = self.feature_manager.create_ui()
self.main_splitter.addWidget(feature_widget)

# In closeEvent (if needed)
if self.feature_manager:
    self.feature_manager.cleanup()
```

#### 4. Add Configuration (if needed)

**In config_manager.py**:
- Add default values
- Add save/load logic

**In bible_search_lite.py**:
- Save settings in `save_config()`
- Restore settings in `load_config()`

#### 5. Document the Feature

Create `Documentation/FEATURE_NAME.md`:
- Overview
- Usage
- Configuration
- Implementation details
- Examples

### Code Style Guidelines

#### Naming Conventions
- **Classes**: PascalCase (`SubjectManager`)
- **Methods**: snake_case (`load_subjects`)
- **Private methods**: Leading underscore (`_format_result`)
- **Constants**: UPPER_SNAKE (`BOOK_GROUPS`)

#### Method Organization
```python
class FeatureManager:
    # 1. __init__
    def __init__(self, ...):
        pass

    # 2. UI creation
    def create_ui(self):
        pass

    # 3. Public methods (alphabetical)
    def add_item(self):
        pass

    def delete_item(self):
        pass

    # 4. Event handlers (on_* methods)
    def on_button_clicked(self):
        pass

    # 5. Helper methods (private)
    def _format_data(self):
        pass

    # 6. Cleanup
    def cleanup(self):
        pass
```

#### Comments
- **Docstrings** for all classes and public methods
- **Inline comments** for complex logic only
- **No commented-out code** (use version control)

#### Error Handling
```python
try:
    # Risky operation
    result = database.query()
except Exception as e:
    print(f"❌ Error: {e}")
    self.parent_app.message_label.setText(f"Error: {e}")
    return None
```

### Testing Approach

#### Manual Testing Checklist
For new features, test:
1. **Happy path** - Feature works as designed
2. **Edge cases** - Empty inputs, max values, etc.
3. **Error conditions** - Database errors, file errors
4. **Integration** - Doesn't break existing features
5. **Persistence** - Settings save and restore correctly

#### Test Files
Create test files in `Utilities/`:
```python
# test_feature.py
import sys
from PyQt6.QtWidgets import QApplication
from bible_search_lite import BibleSearchProgram

def test_feature():
    """Test specific feature"""
    app = QApplication(sys.argv)
    window = BibleSearchProgram()
    window.show()

    # Perform test actions
    # Check results

    app.exec()

if __name__ == "__main__":
    test_feature()
```

### Debugging Tips

#### Print Debugging
Use emoji prefixes for visibility:
```python
print(f"🔍 Search query: {query}")
print(f"✅ Success: {result}")
print(f"❌ Error: {error}")
print(f"📊 Count: {count}")
```

#### Common Issues

**Fonts not applying**:
- Check `setup_styling()` in widgets.py
- Ensure `apply_font_settings()` called after loading verses
- Verify font size lookup from main_window

**Window not visible**:
- Check splitter sizes in config (may be 0)
- Verify `setVisible(True)` called
- Check if added to splitter

**Settings not persisting**:
- Verify `save_config()` called in `closeEvent`
- Check config file exists and is writable
- Ensure `load_config()` called in `__init__`

**Database errors**:
- Check table exists (`init_subjects_database.py`)
- Verify foreign keys defined
- Use transactions for multi-step operations

---

## Bug Fixes and Known Issues

### Recent Bug Fixes (v3.0)

#### 1. Font Size Persistence Bug
**Problem**: Fonts reset to 9pt when clicking verses, even though settings showed 10pt

**Root Cause**: `setup_styling()` in widgets.py hardcoded `font.setPointSizeF(9)`. When verses unhighlighted, it reset fonts.

**Fix**: Modified `setup_styling()` to traverse widget tree to find main_window and use saved font size instead of hardcoding.

**Location**: `bible_search_ui/ui/widgets.py` lines 169-180

**Status**: ✅ Fixed

#### 2. Window 1 Hidden Bug
**Problem**: Message window collapsed to 0 height, became invisible

**Root Cause**: Splitter sizes in config had `[140, 0, 436]` - second value was 0

**Fix**: Reset splitter sizes in config to `[80, 200, 300]`

**Status**: ✅ Fixed

#### 3. Toggle Button State Bug
**Problem**: 📑 button stayed green when Windows 4 & 5 closed

**Root Cause**: `show()` and `hide()` methods didn't update button state

**Fix**: Added button state updates in both methods
```python
self.parent_app.subject_toggle_btn.setChecked(True/False)
self.parent_app.update_subject_toggle_style(True/False)
```

**Location**: `subject_manager.py` lines 124-127, 143-146

**Status**: ✅ Fixed

#### 4. Settings Not Persisting
**Problem**: Checkbox states and font sizes not restored on startup

**Root Cause**: `load_config()` only loaded search history

**Fix**: Enhanced `load_config()` to restore:
- Window geometry
- Splitter sizes
- Checkbox states
- Font settings

**Location**: `bible_search_lite.py` lines 3192-3219

**Status**: ✅ Fixed

#### 5. Subject Dropdown Not Clearing
**Problem**: Subject selection persisted across app restarts

**Fix**: Added `setCurrentIndex(0)` in `closeEvent()`

**Location**: `bible_search_lite.py` lines 3247-3258

**Status**: ✅ Fixed

### Known Issues

#### 1. Large Search Results Performance
**Issue**: Searches returning >5000 results may be slow to display

**Workaround**: Use filters to narrow results

**Future Fix**: Implement virtual scrolling (lazy loading)

**Priority**: Medium

#### 2. Cross-Reference Navigation
**Issue**: Cross-reference dropdown works but could be more intuitive

**Enhancement**: Add tooltips, preview on hover

**Priority**: Low

#### 3. Subject Import/Export
**Issue**: Can export subjects but can't import them back

**Enhancement**: Add import feature to restore subjects from CSV/RTF

**Priority**: Medium

---

## Future Enhancements

### Planned Features

#### 1. Advanced Search
- **Proximity search**: Find words within N words of each other
- **Root word search**: Search by Greek/Hebrew roots
- **Regex support**: Full regular expression support
- **Priority**: High

#### 2. Study Tools
- **Concordance**: Word frequency analysis
- **Topical index**: Browse topics and related verses
- **Reading plans**: Daily reading schedules
- **Priority**: Medium

#### 3. Export Enhancements
- **PDF export**: Direct PDF generation
- **HTML export**: Web-friendly format
- **Email integration**: Send exports via email
- **Cloud storage**: Save to Google Drive, Dropbox
- **Priority**: Medium

#### 4. Subject Enhancements
- **Subject groups**: Organize subjects into categories
- **Subject import**: Import subjects from CSV/RTF
- **Shared subjects**: Export/import for sharing with others
- **Tags**: Tag verses within subjects
- **Priority**: High

#### 5. UI Improvements
- **Dark mode**: Dark color scheme option
- **Customizable layout**: Drag-and-drop window arrangement
- **Multiple windows**: Open multiple search windows
- **Tabs**: Tab-based interface option
- **Priority**: Low

#### 6. Collaboration Features
- **Cloud sync**: Sync subjects across devices
- **Sharing**: Share subjects with other users
- **Comments**: Collaborate on verse comments
- **Priority**: Low (requires backend)

### Technical Debt

#### 1. Code Cleanup
- Remove deprecated methods (marked in code)
- Consolidate duplicate code
- Improve error handling

#### 2. Testing
- Add unit tests for core functionality
- Add integration tests
- Add UI automation tests

#### 3. Documentation
- Add inline documentation for complex methods
- Create video tutorials
- Create API documentation for developers

#### 4. Performance
- Optimize database queries
- Add query caching
- Implement virtual scrolling

---

## Appendix A: Quick Reference

### Keyboard Shortcuts
- **Ctrl+F**: Focus search box
- **Ctrl+C**: Copy (when verses selected)
- **Enter**: Perform search (when in search box)
- **Esc**: Clear selection

### Search Operators
- `*` - Wildcard (matches any characters)
- `AND` - Both terms must appear
- `OR` - Either term must appear
- `"..."` - Exact phrase match

### File Locations
- **Config**: `bible_search_lite_config.json`
- **Bible DB**: `database/bibles.db`
- **Subjects DB**: `database/subjects.db`
- **Exports**: `downloads/` (default)
- **Logs**: Terminal output only

### Support Files
- **Launch script**: `run_bible_search.sh`
- **Database init**: `Utilities/init_subjects_database.py`
- **Documentation**: `Documentation/` folder

---

## Appendix B: Troubleshooting

### Application Won't Start
1. Check Python version: `python3 --version` (need 3.8+)
2. Check PyQt6 installed: `pip list | grep PyQt6`
3. Check database exists: `ls database/bibles.db`
4. Try: `bash run_bible_search.sh`

### Window Not Visible
1. Check config file splitter sizes
2. Reset config: Delete `bible_search_lite_config.json`
3. Restart app

### Search Not Working
1. Check database: `sqlite3 database/bibles.db "SELECT COUNT(*) FROM bible_verses;"`
2. Check translations selected
3. Check search syntax (see Search Operators)

### Subjects Not Saving
1. Check subjects database: `ls database/subjects.db`
2. If missing, run: `python3 Utilities/init_subjects_database.py`
3. Check file permissions

### Export Failing
1. Check downloads folder exists and is writable
2. Try different export location
3. Check disk space
4. Try simpler export (fewer verses, CSV instead of RTF)

---

## Version History

### v3.0 (December 29, 2025)
- ✅ Modular architecture (Subject management separated)
- ✅ Export feature (CSV, RTF, Printer)
- ✅ Enhanced search status messages
- ✅ Subject sync feature
- ✅ Font persistence fixes
- ✅ Settings persistence improvements
- ✅ Help system with export documentation

### v2.0 (December 27, 2025)
- ✅ Windows 4 & 5 implementation (monolithic)
- ✅ Subject database integration
- ✅ Rich-text comment editor
- ✅ Toggle visibility for Windows 4 & 5

### v1.0 (December 2025)
- ✅ Core search functionality
- ✅ Multi-translation support
- ✅ Context viewing (Window 3)
- ✅ Basic UI (Windows 1-3)

---

**End of Documentation**

For questions, issues, or feature requests, create documentation in `Documentation/` folder or add comments in code.
