# Bible Search Lite v1.1.3 Release Notes

**Release Date:** January 29, 2026

## Bug Fixes

### Apostrophe Search Support
- **Fixed inability to search for words with apostrophes**
  - Issue: Searches for words like "father's", "mother's", "Lord's" returned 0 results
  - Root cause: Database uses Unicode right single quotation mark (U+2019 ') instead of standard apostrophe (U+0027 ')
  - Fix: Added automatic character normalization that converts standard apostrophes to U+2019 in all search queries and highlighting
  - Now searches for "father's" correctly return all 137 matching verses
  - Highlighting also works correctly for apostrophe-containing words

### Apostrophe Highlighting
- **Fixed green highlighting not appearing on apostrophe words**
  - Issue: Searching for "father's house" highlighted "house" in green but "father's" only had brackets, not green color
  - Root cause: `extract_highlight_terms()` wasn't normalizing apostrophes before passing to UI highlighting
  - Fix: Added apostrophe normalization to `extract_highlight_terms()` method
  - Now both "father's" and "house" are highlighted in green with brackets

## Technical Details

### Implementation
- Added apostrophe normalization in all query building methods:
  - `build_word_search_query()` - main search query builder
  - `_build_proximity_query()` - for proximity searches (~N)
  - `_build_ordered_words_query()` - for ordered word searches (>)
  - `_build_word_placeholder_query()` - for placeholder searches (&)
  - `highlight_search_terms()` - for result highlighting
- Normalization converts U+0027 (') to U+2019 (') using `query.replace("'", "\u2019")`
- Applied consistently across all search types and highlighting

### Character Details
- **Standard apostrophe:** U+0027 (') - what users type on keyboards
- **Right single quotation mark:** U+2019 (') - what's stored in the database
- The normalization is automatic and transparent to users

## Testing

Verified functionality:
1. Search for "father's" - returns 137 results ✓
2. Highlighting of "father's" - shows `[father's]` brackets ✓
3. Multi-word search "father's house" - returns 70 results with proper highlighting ✓
4. Works with all search operators (AND, OR, wildcards, etc.) ✓

## Examples

Previously failed, now work:
- `father's` - finds "father's house", "father's servants", etc.
- `Lord's` - finds "Lord's commandments", "Lord's house", etc.
- `mother's` - finds "mother's sons", "mother's womb", etc.
- `David's` - finds "David's house", "David's men", etc.

## Upgrade Notes

- No database schema changes
- No breaking changes to existing queries
- All existing queries continue to work as before
- Apostrophe searches now work automatically

## Files Changed

- `bible_search.py` - Added apostrophe normalization to 5 methods
- `bible_search_lite.py` - Version bump to v1.1.3 and added normalization to `extract_highlight_terms()`
- `VERSION.txt` - Updated to v1.1.3

---

For questions or issues, please report at: https://github.com/anthropics/bible-search-lite/issues
