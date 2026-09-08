# Release Notes - Bible Search Lite v1.1.6

**Release Date:** September 8, 2026

## What's New

### Select Books dialog
- New **Select Books...** entry on the book filter menu opens a dialog with a
  checkbox for every book of the Bible, grouped by testament, with Check All
  and Uncheck All buttons for each group
- The dialog opens pre-checked with whatever the current filter includes, so a
  group such as "Prophets" can be adjusted book by book
- Any selection that is not a whole group becomes a "Custom Selection" filter

### Biblical order for scripture lists
- Copying, printing and exporting a scripture list now sorts the verses by
  book, chapter and verse instead of the order they were added
- Verse references in exports can include or omit the translation code

### Lighter, flatter look for all five windows
- The raised bevelled frames around each window (5 pixels) and around each
  verse list (3 pixels) are replaced by a single 1 pixel line, the frame
  margins are gone so the splitter bars line up with the edges, and the outer
  margin of the main window is down from about 11 pixels to 3
- Window headers are now 10 point, normal weight, medium grey (still blue on
  hover, still clickable); the active window is still marked by its blue outline
- Splitter bars are flat 4 pixel grey bars with the green hover kept
- Background lifted slightly from #f0f0f0 to #f4f4f4; button rows in Windows 4
  and 5 use 3 pixel padding instead of 5

### Brenton Septuagint (BST) re-imported
- The Brenton translation was missing ten books (1 and 2 Samuel, 1 and 2 Kings,
  1 and 2 Chronicles, Esther, Daniel, Joel and Nahum) and the first verse of
  every chapter in the books it did have. It has been re-imported in full from
  the eBible.org public domain edition: 23,475 verses, up from 17,902
- Brenton follows Septuagint numbering (Psalm 34 in BST is Psalm 35 in the
  KJV), and its extra verses (for example the Song of the Three in Daniel 3)
  now appear in BST only
- **This change lives in `bibles.db`.** Download the new database from this
  release; `database/DOWNLOAD_DATABASE.md` now points at v1.1.6

### In-app updater now updates every file
- **File > Check for Updates** used to replace only `bible_search_lite.py`, which
  left the program unable to start when a release also changed one of the
  modules it imports (as this one does). The updater now downloads every
  application file listed in `update_files.txt` on GitHub, installs them only
  once all have arrived, and keeps the previous files in `update_backup/`
- Version numbers are now compared numerically, so 1.1.10 will count as newer
  than 1.1.9
- Users updating **from 1.1.5 or earlier** are still running the old updater and
  will hit the import error once; see Upgrade Notes below

## Bug Fixes
- Fixed: in-app update from 1.1.5 left an ImportError (BookSelectorDialog) because
  only the main file was replaced

- Fixed: Brenton (BST) showed no text for Daniel and nine other books
- Fixed: Brenton (BST) was missing verse 1 of every chapter

## Housekeeping

- `.claude/worktrees/` is now ignored by git
- Version bumped to 1.1.6 in `bible_search_lite.py`, `setup.py`,
  `setup_win11.py` and `VERSION.txt`

## Upgrade Notes

**If you used File > Check for Updates from 1.1.5 and the program no longer
starts** (ImportError: cannot import name 'BookSelectorDialog'), the old updater
replaced only the main file. Either run the installer again in the same folder
(`python setup_win11.py` on Windows, `python3 setup.py` elsewhere), which
refreshes every file and keeps your `subjects.db`, or download these files from
GitHub into your installation, keeping the folder structure:
`bible_search_ui/ui/dialogs.py`, `bible_search_ui/ui/widgets.py`,
`export_dialog.py`, `subject_verse_manager.py`. Future updates will not have
this problem.

For the Brenton (BST) fix, replace `database/bibles.db` with the file attached
to the v1.1.6 release, or rerun the installer. Your `subjects.db` and
`user_data.db` are not affected.

See all commits at: https://github.com/andyinva/bible-search-lite/compare/v1.1.5...v1.1.6
