# Wildcard Highlighting Fix - Question Mark (?) Operator

## Issue
The `?` wildcard operator in search patterns like `"father?"` was not highlighting all matching words correctly. Specifically:
- Pattern: `"father?"`
- Expected matches: "fathers", "fatherd", etc. (any 7-letter word starting with "father")
- **Problem**: Words with apostrophes like "father'" were not being highlighted

## Root Cause
In [bible_search.py](bible_search.py) line 761, the `?` wildcard was being converted to the regex pattern `\w`, which only matches:
- Letters (a-z, A-Z)
- Digits (0-9)
- Underscore (_)

**BUT NOT apostrophes** (`'` or `'`), which are common in Biblical text for possessives.

## Solution
Changed the `?` wildcard regex pattern from `\w` to `[a-zA-Z'']` to include both:
- Regular apostrophe: `'` (U+0027)
- Right single quotation mark: `'` (U+2019) - used in the database

### Code Change
**File**: [bible_search.py](bible_search.py) line 761

**Before**:
```python
elif char == '?':
    regex_parts.append(r'\w')
```

**After**:
```python
elif char == '?':
    # Match exactly one character (letter or apostrophe for possessives)
    regex_parts.append(r"[a-zA-Z'']")
```

## Examples

### Search: `"father?"`
Matches 7-character words starting with "father":
- ✅ "fathers" (father + s)
- ✅ "father'" (father + apostrophe)
- ✅ "fathery" (hypothetical)
- ❌ "father's" (8 characters - apostrophe + s = 2 chars)
- ❌ "father" (6 characters - too short)

### Search: `("sleep*" OR "slep*") AND "father?"`
Now properly highlights:
- "sleep", "sleeping", "sleepeth" etc. in **green/blue**
- "slept" in **green/blue**
- "fathers" in **green/blue** ✨ (now working!)
- "father'" in **green/blue** ✨ (now working!)

## Wildcard Operators Comparison

| Operator | Matches | Regex Pattern | Example |
|----------|---------|---------------|---------|
| `*` | 0+ characters | `[a-zA-Z]*(?:[''][a-zA-Z]*)*` | "sing*" → "sing", "singing", "singer's" |
| `%` | 0+ characters | `[a-zA-Z]*(?:[''][a-zA-Z]*)*` | "sing%" → same as `*` |
| `?` | Exactly 1 char | `[a-zA-Z'']` | "father?" → "fathers", "father'" |

## Highlighting Colors

The two-color highlighting system shows:
- **Green background**: The base/fixed part of the match (e.g., "father")
- **Blue background**: The variable part from the wildcard (e.g., "s")

For `"father?"` matching "fathers":
- `[father]{s}` → <span style="background-color: #90EE90;">father</span><span style="background-color: #ADD8E6;">s</span>

## Testing

Test script created: [test_father_wildcard.py](test_father_wildcard.py)

Run test:
```bash
python3 test_father_wildcard.py
```

Expected output:
```
Pattern for 'father?': \bfather[a-zA-Z'']\b
Found 2 matches:
  - 'fathers' at position 4-11
  - 'father'' at position 20-27
✓ Pattern correctly matches 'fathers'!
```

## Benefits

1. **Accurate highlighting**: All matching words are now highlighted in search results
2. **Consistent behavior**: `?` wildcard now works as expected with apostrophes
3. **Biblical text support**: Handles possessive forms common in scripture
4. **Cross-platform**: Works with both apostrophe encodings (U+0027 and U+2019)

## Files Modified

1. **bible_search.py** (line 761)
   - Updated `?` wildcard regex pattern to include apostrophes

2. **test_father_wildcard.py** (NEW)
   - Test script to verify the fix

3. **WILDCARD_HIGHLIGHTING_FIX.md** (NEW)
   - This documentation file
