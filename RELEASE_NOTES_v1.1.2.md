# Bible Search Lite v1.1.2 Release Notes

**Release Date:** January 29, 2026

## New Features

### Parentheses Support for Operator Precedence
- **Added parentheses `( )` to control AND/OR operator precedence**
  - Example: `("sleep*" OR "slep*") AND father` - finds verses with father AND either sleep word
  - Without parentheses: `"sleep*" OR "slep*" AND father` - evaluates as `"sleep*" OR ("slep*" AND father)` due to AND having higher precedence
  - Allows complex boolean queries with clear operator precedence
  - Works with all search terms including quoted phrases and wildcards

## Bug Fixes

### Search Functionality
- **Fixed OR operator with wildcards** - OR queries now correctly apply wildcard word boundary filtering
  - Issue: `"sleep*" OR "slep*"` was requiring ALL terms to match instead of ANY term
  - Fix: Added detection of OR operator and changed wildcard filtering logic from AND to OR

- **Fixed "AND" being highlighted as search term**
  - Issue: When searching `"sleep*" OR "slep*" AND father`, the word "and" was highlighted in green
  - Fix: Improved regex for splitting on AND/OR operators from `\s+(?:AND|OR)\s+` to `\b(?:AND|OR)\b`

- **Fixed missing highlight brackets in search results**
  - Issue: Search terms were highlighted in green but brackets `[ ]` were missing
  - Fix: Added brackets around matched terms in highlighting code

### Window 3 (Reading Window) Features
- **Fixed "Go Back" button to restore both references and verses**
  - Issue: Go Back button restored References dropdown but Window 3 showed blank screen
  - Fix: Save Window 3 verse list state before clearing, then restore both references and verses when going back
  - Now properly saves and restores: verse text, translation, highlighting state, and cross-references

## Documentation Updates

### SEARCH_OPERATORS.md
- Added comprehensive section on parentheses usage
- Updated "Combining Operators" section with parentheses examples
- Added parentheses to Quick Reference Table
- Explained operator precedence and why parentheses are needed

### Help Menu
- Added parentheses section to Boolean Operators
- Included visual examples showing with/without parentheses behavior
- Updated "Combining Operators" with complex query examples
- Added note that parentheses only work with AND/OR, not with special operators (>, ~, &)

## Technical Details

### Implementation
- Parentheses are detected in `build_word_search_query()` and processed by `_build_query_with_parentheses()`
- Simple implementation wraps OR expressions in SQL parentheses when AND follows
- Supports single level of parentheses grouping: `(A OR B) AND C`
- More complex nested parentheses may require future enhancements

### Wildcard Filtering
- Added `_query_uses_or` flag to detect OR queries
- Updated `_matches_wildcard_word_boundaries()` to use OR logic (ANY match) vs AND logic (ALL match)
- Ensures wildcard terms like `"sleep*"` properly match with word boundaries in OR queries

## Upgrade Notes

- No database schema changes
- No breaking changes to existing queries
- All existing queries continue to work as before
- New parentheses feature is optional and backwards compatible

## Known Limitations

- Parentheses only support one level of grouping: `(A OR B) AND C`
- Complex nested parentheses like `((A OR B) AND C) OR D` are not yet supported
- Parentheses only work with AND/OR operators, not with special operators (>, ~, &)

## Files Changed

- `bible_search.py` - Added parentheses support and fixed OR operator wildcard filtering
- `bible_search_lite.py` - Version bump and Help menu updates
- `bible_search_ui/ui/widgets.py` - No changes
- `SEARCH_OPERATORS.md` - Added parentheses documentation
- `VERSION.txt` - Updated to v1.1.2

## Testing

Recommended test queries:
1. `("sleep*" OR "slep*") AND father` - should return ~40 verses, all with "father"
2. `("faith" OR "belief") AND works` - should return verses with works AND either term
3. `"sleep*" OR "slep*"` - should return all verses with either wildcard (no AND filtering)
4. Test Go Back button after clicking cross-references - should restore previous state

---

For questions or issues, please report at: https://github.com/anthropics/bible-search-lite/issues
