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

## Bug Fixes

- Fixed: Brenton (BST) showed no text for Daniel and nine other books
- Fixed: Brenton (BST) was missing verse 1 of every chapter

## Housekeeping

- `.claude/worktrees/` is now ignored by git
- Version bumped to 1.1.6 in `bible_search_lite.py`, `setup.py`,
  `setup_win11.py` and `VERSION.txt`

## Upgrade Notes

Pull the code, then replace `database/bibles.db` with the file attached to the
v1.1.6 release. Your `subjects.db` and `user_data.db` are not affected.

See all commits at: https://github.com/andyinva/bible-search-lite/compare/v1.1.5...v1.1.6
