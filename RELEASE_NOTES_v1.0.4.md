# Bible Search Lite v1.0.4 Release Notes

**Release Date:** January 10, 2026

## What's New in v1.0.4

### 🎯 Enhanced Verse Highlighting

- **Visual Feedback for Clicked Verses**: Verses in Window 3 (Reading Window) now highlight in gray when clicked, making it easy to see which verse is active for cross-reference lookup
- **Smart Highlight Management**: Only one verse is highlighted at a time across all windows - previous highlights are automatically cleared when clicking a new verse
- **Seamless Navigation**: Clicking verses in Window 2 or Window 3 now provides consistent visual feedback

### 🖱️ Improved Window Interaction

- **Click Anywhere to Activate**: Window 2 (Search Results) now activates when you click anywhere in it, not just on the sidebar
- **Better Event Handling**: Added event filter for QListWidget viewport to capture all mouse clicks reliably

### 🐛 Bug Fixes

- **Fixed Persistent Highlights**: Resolved issue where blue-highlighted verses from Window 2 clicks would remain highlighted when clicking verses in Window 3
- **Unified Styling System**: Created a single styling method that properly handles all verse states (highlighted, checked, normal) with correct priority
- **Cross-Window State Management**: Highlights now properly clear across both Window 2 and Window 3

### 🔧 Technical Improvements

- Added `is_highlighted` property to track navigation highlights separately from checkbox selection
- Created `apply_current_style()` method with proper state priority: highlighted → checked → normal
- Enhanced `set_highlighted_verse()` to clear both old blue highlights and new gray highlights
- Improved event propagation for more reliable click detection

## Upgrade Instructions

### Automatic Update (Recommended)

1. Click the "Check for Updates" button in the Help menu
2. If prompted, click "Download Update"
3. The new version will be downloaded and applied automatically

### Manual Update

1. Download the latest release from: https://github.com/andyinva/bible-search-lite
2. Extract the files to your bible-search-lite directory
3. Run `python3 bible_search_lite.py`

## Previous Versions

- [v1.0.3](RELEASE_NOTES_v1.0.3.md) - Auto-update improvements and enhanced setup script
- [v1.0.2](RELEASE_NOTES_v1.0.2.md) - Version display in window title
- [v1.0.1](RELEASE_NOTES_v1.0.1.md) - Initial release

---

For full documentation, see [README.md](README.md)

For installation instructions, see [INSTALLATION.md](INSTALLATION.md)
