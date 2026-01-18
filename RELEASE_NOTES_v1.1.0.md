# Bible Search Lite v1.1.0 Release Notes

**Release Date:** January 18, 2026

This is a major feature release that introduces a hierarchical book menu, translation name display in the Reading Window, complete publication dates for all Bible translations, and a comprehensive offline Windows installer.

---

## 🎉 New Features

### Hierarchical Book Filter Menu
- **Two-level menu navigation** - Old Testament and New Testament now expand to show individual books
- Select entire testament or specific books from expandable submenus
- Visual hierarchy makes it easier to navigate 66+ Bible books
- Testament selections show abbreviated display (OT/NT) in button
- Book filter selection now persisted in configuration

**Before:** Simple dropdown with pre-grouped categories
**After:** Hierarchical menu with expandable Old/New Testament submenus

### Translation Display in Reading Window
- **Translation name and date shown in Reading Window header**
- Displays to the right of "Reading Window" title
- Styled to match window title (bold, consistent formatting)
- Format: "Translation Name (Publication Year)"
- Example: "King James Bible (1611)"
- Automatically updates when clicking verses from different translations
- Clears when Reading Window is cleared

### Complete Translation Publication Dates
- **Added 24+ missing publication dates** for Bible translations
- All translations now display with their publication years
- Dates extracted from database descriptions with fallback to hardcoded lookup
- Clean, consistent formatting across all translations

**Translations with added dates:**
- DRB (1582-1610), DBT (1890), WEB (2000), WNT (1903)
- NET (2005), ACV (2008), BSB (2016), CPD (2009)
- DRC (1749-52), LEB (2012), LIT (1985)
- NHE (2023), NHJ (2023), NHM (2023)
- OEB (2010), OEC (2010), TWE (1904)
- MKJ (1998), BST (1844), BBE (1965)
- JPS (1917), ROT (1902), YLT (1862), JUB (2000)

### Search Button Dynamic Styling
- Search button turns **blue** when search box has text (active state)
- Search button turns **gray** when search box is empty (inactive state)
- Real-time style updates as you type
- Visual feedback helps users know when search is ready

### Windows Offline Installer Package
- **Complete offline installation system** for Windows 10/11
- Two-phase process: download on internet PC, install on offline PC
- Self-contained Python 3.12.1 + PyQt6 installation
- Works on air-gapped systems and high-security environments
- Automated installer with desktop shortcut creation
- Comprehensive documentation (8 files, 1,194 lines)

**Installer Features:**
- Downloads ~85 MB of dependencies (Python + PyQt6)
- Installs to isolated directory (won't affect system Python)
- Creates desktop shortcut automatically
- Includes uninstaller
- PowerShell scripts + batch file alternative
- Complete documentation with troubleshooting guide

---

## 🔧 Improvements

### Translation Name Handling
- Changed from database `name` field to `description` field for better formatting
- Smart date extraction using regex patterns
- Hardcoded lookup table for translations without dates in description
- Eliminates "Imported from MIT Bible Database" extraneous text
- Consistent formatting: "Name (Year)" across all translations

### Book Filter Enhancement
- Changed from QComboBox to QPushButton with QMenu
- Testament selections abbreviated (OT/NT) to save space
- Individual book selections display full book name
- Filter selection saved in configuration file
- Improved visual hierarchy and navigation

### UI Polish
- Translation label styled to match window titles (bold, 11px)
- Translation label clears appropriately when reading window cleared
- Filter button minimum width set to accommodate 3-digit counts
- Proper hasattr checks prevent AttributeError exceptions

---

## 🐛 Bug Fixes

### Critical Fixes
- **Fixed AttributeError** when loading context verses in Reading Window
  - Changed from non-existent `trans.name` to `trans.full_name`
  - Added proper attribute existence checks
  - Prevents crashes when clicking verses

### Error Handling
- Added `hasattr()` checks for `translation_label` attribute
- Proper null/None handling in translation display code
- Safe fallback to abbreviation if translation not found

---

## 📁 Files Changed

### Core Application
- `bible_search.py` - Translation loading with dates (+83 lines)
- `bible_search_lite.py` - Hierarchical menu, translation display (+407 lines)
- `bible_search_ui/ui/dialogs.py` - Filter dialog improvements (+54 lines)
- `bible_search_ui/ui/widgets.py` - SectionWidget translation label (+21 lines)

### New: Windows Installer Package
- `win_install/01_download_dependencies.ps1` - Dependency downloader
- `win_install/02_install_offline.ps1` - Offline installer
- `win_install/INSTALL.bat` - Batch file launcher
- `win_install/README.md` - Complete documentation
- `win_install/QUICK_START.txt` - Quick reference
- `win_install/CHECKLIST.txt` - Step-by-step guide
- `win_install/PROCESS_DIAGRAM.txt` - Visual workflow
- `win_install/START_HERE.txt` - Navigation guide

**Total Changes:**
- 12 files changed
- 1,665+ lines added
- 94 lines removed

---

## 💾 Installation

### Standard Installation (with internet)
Download and install as usual - see main README.md

### Offline Installation (Windows)
1. On internet PC: Run `win_install/01_download_dependencies.ps1`
2. Copy `win_install` folder to USB drive
3. On target PC: Run `win_install/INSTALL.bat` as Administrator
4. Launch from desktop shortcut

See `win_install/README.md` for complete offline installation guide.

---

## 🔄 Upgrade from 1.0.4

No database changes required - simply replace the application files.

Your configuration will be preserved:
- Search history
- Selected translations
- Window sizes and positions
- Font settings
- Book filter selection

---

## 📊 Statistics

- **Version:** 1.1.0
- **Release Type:** Minor (new features)
- **Lines of Code Added:** 1,665+
- **Files Changed:** 12
- **New Features:** 5 major
- **Bug Fixes:** 2 critical
- **Documentation:** 8 new files
- **Translation Dates Added:** 24+

---

## 🎯 Highlights

### For Users
✅ Easier book navigation with hierarchical menus
✅ See which translation you're reading in Window 3
✅ All translations now show publication dates
✅ Visual feedback on search button state
✅ Offline installation option for air-gapped PCs

### For IT Administrators
✅ Complete offline installer for secure environments
✅ Isolated Python installation (won't affect system)
✅ Automated deployment ready
✅ Comprehensive documentation
✅ Uninstaller included

---

## 🔮 Future Plans

Planned for future releases:
- Additional Bible translations
- Export functionality improvements
- Advanced search operators
- Theme customization options
- Cross-reference enhancements

---

## 🙏 Acknowledgments

- Python 3.12.1 - Core runtime
- PyQt6 - GUI framework
- SQLite - Database engine
- Community feedback and testing

---

## 📝 License

Bible Search Lite is open source software.
See LICENSE file for details.

---

## 🔗 Links

- **GitHub Repository:** https://github.com/andyinva/bible-search-lite
- **Issues:** https://github.com/andyinva/bible-search-lite/issues
- **Documentation:** See README.md in repository

---

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check the documentation in the repository
- Review the troubleshooting guides

---

**Generated with Claude Code**

**Co-Authored-By:** Claude <noreply@anthropic.com>
