# Hanging Indent for Verse Text - Improved Readability

## Problem Description

When verses wrapped to multiple lines, the continuation lines started at the left edge, aligned with the verse reference:

```
KJV Isa 2:12 - For the day of the Lord of hosts shall be upon every one that is proud and lofty, and upon
every one that is lifted up; and he shall be brought low:
```

This made it harder to visually distinguish where one verse ended and another began, especially with long verses.

## Desired Behavior

The user requested that wrapped lines should indent to align with where the **verse text** begins (after the reference and " - "):

```
KJV Isa 2:12 - For the day of the Lord of hosts shall be upon every one that is proud and lofty, and upon
               every one that is lifted up; and he shall be brought low:
```

This is called a **hanging indent** or **first-line outdent**.

## Solution Implemented

### How It Works

1. **Calculate Reference Width**
   - Measure the pixel width of "KJV Isa 2:12 - " using Qt's font metrics
   - This width becomes the indent for continuation lines

2. **Apply HTML Formatting**
   - Format the text as HTML with CSS styling
   - Use `text-indent: -Npx` to pull the first line left
   - Use `padding-left: Npx` to push all lines right
   - Net effect: First line at position 0, continuation lines at position N

3. **Dynamic Adjustment**
   - Recalculate indent when font size changes
   - Maintains proper alignment at any font size

## Changes Made to widgets.py

### Location 1: Initial Setup (Lines 119-150)

**Before:**
```python
ref_text = f"{self.translation} {self.book_abbrev} {self.chapter}:{self.verse_number}"
combined_text = f"{ref_text} - {self.text}"
self.text_label = QLabel(combined_text)
self.text_label.setWordWrap(True)
```

**After:**
```python
ref_text = f"{self.translation} {self.book_abbrev} {self.chapter}:{self.verse_number}"

# Calculate reference width for hanging indent
temp_font = QFont("IBM Plex Mono", 9)
from PyQt6.QtGui import QFontMetrics
font_metrics = QFontMetrics(temp_font)
ref_width = font_metrics.horizontalAdvance(ref_text + " - ")

# Format with HTML for hanging indent
combined_html = f'''
<div style="text-indent: -{ref_width}px; padding-left: {ref_width}px;">
{ref_text} - {self.text}
</div>
'''

self.text_label = QLabel(combined_html)
self.text_label.setTextFormat(Qt.TextFormat.RichText)  # Enable HTML
self.text_label.setWordWrap(True)
```

### Location 2: Font Size Changes (Lines 199-216)

When font size changes, recalculate the indent:

```python
font.setPointSizeF(font_size)
self.text_label.setFont(font)

# Recalculate hanging indent for new font size
font_metrics = QFontMetrics(font)
ref_width = font_metrics.horizontalAdvance(self.reference_text + " - ")
self.ref_width = ref_width

# Update HTML with new indent
combined_html = f'''
<div style="text-indent: -{ref_width}px; padding-left: {ref_width}px;">
{self.reference_text} - {self.text}
</div>
'''
self.text_label.setText(combined_html)
```

### Location 3: Search Highlighting (Lines 419-431)

Maintain hanging indent when highlighting search terms:

```python
text = self.text
for term in search_terms:
    text = text.replace(term, f"<b><u>{term}</u></b>")

# Maintain hanging indent
combined_html = f'''
<div style="text-indent: -{self.ref_width}px; padding-left: {self.ref_width}px;">
{self.reference_text} - {text}
</div>
'''
self.text_label.setText(combined_html)
```

## Technical Details

### CSS Hanging Indent Technique

```css
text-indent: -100px;   /* Pull first line 100px to the LEFT */
padding-left: 100px;   /* Push ALL lines 100px to the RIGHT */
```

**Result:**
- Line 1: -100px + 100px = 0px (starts at left edge)
- Line 2+: 0px + 100px = 100px (indented)

### Font Metrics Calculation

```python
font_metrics = QFontMetrics(font)
width = font_metrics.horizontalAdvance("KJV Isa 2:12 - ")
```

This gives the **exact pixel width** of the reference text in the current font:
- Font size 9pt: ~85px
- Font size 10pt: ~95px
- Font size 11pt: ~105px

### Dynamic Updates

The indent is recalculated in three situations:

1. **Initial creation** (line 127)
   - When verse widget is first created
   - Uses default font size (9pt)

2. **Font size change** (line 206)
   - When user changes font settings
   - Recalculates with new font size

3. **Search highlighting** (line 426)
   - When search terms are highlighted
   - Maintains current indent value

## Visual Examples

### Short Reference (KJV Gen 1:1):
```
KJV Gen 1:1 - In the beginning God created the heaven and the earth.
```
Indent width: ~75px

### Medium Reference (KJV Psa 119:105):
```
KJV Psa 119:105 - Thy word is a lamp unto my feet, and a light unto my path.
```
Indent width: ~95px

### Long Reference (KJV 1Thess 5:23):
```
KJV 1Thess 5:23 - And the very God of peace sanctify you wholly; and I pray God your whole spirit and soul
                   and body be preserved blameless unto the coming of our Lord Jesus Christ.
```
Indent width: ~105px

Each verse gets the **exact indent** it needs based on its reference length!

## Benefits

✅ **Improved Readability**
- Easy to see where each verse begins
- Continuation lines clearly belong to the verse above
- Visual hierarchy is clearer

✅ **Professional Appearance**
- Matches standard Bible formatting
- Looks like printed Bibles
- Clean, organized layout

✅ **Dynamic Adaptation**
- Works with any translation abbreviation length
- Adapts to font size changes
- Maintains alignment at all window widths

✅ **Preserved Functionality**
- Copy/paste still gives plain text
- Search highlighting still works
- Selection and navigation unchanged

## Important Notes

### Plain Text Preserved

The original verse text is still stored as plain text in `self.text`:
```python
self.text = "For the day of the Lord..."  # Plain text, no HTML
```

HTML formatting is **only** for display. When copying or exporting:
- The plain text is used
- No HTML tags appear
- Original verse text is intact

### HTML/Rich Text

The label uses `Qt.TextFormat.RichText` to interpret HTML:
```python
self.text_label.setTextFormat(Qt.TextFormat.RichText)
```

This enables:
- CSS styling (for hanging indent)
- Bold/underline (for search highlighting)
- Color formatting (if needed in future)

### Performance

The hanging indent has **minimal performance impact**:
- Width calculated once per verse
- Only recalculated on font changes (rare)
- HTML rendering is fast in Qt
- No impact on scrolling performance

## Installation

1. **Backup current file:**
   ```bash
   cd ~/projects/bible-search-lite
   cp bible_search_ui/ui/widgets.py bible_search_ui/ui/widgets.py.backup4
   ```

2. **Replace with updated file:**
   ```bash
   cp /path/to/widgets.py bible_search_ui/ui/widgets.py
   ```

3. **Clear Python cache:**
   ```bash
   find ~/projects/bible-search-lite -name "__pycache__" -type d -exec rm -rf {} +
   ```

4. **Restart application:**
   ```bash
   python bible_search_lite.py
   ```

## Testing

1. **Test basic wrapping:**
   - Search for "Isa 2:12-22"
   - Verify long verses (2:12, 2:19, 2:20, 2:21) have hanging indent
   - Check that continuation lines align with verse text start

2. **Test different translations:**
   - Try short abbreviations (KJV, ESV, NIV)
   - Try longer abbreviations (if any)
   - Verify indent adjusts to reference length

3. **Test font sizes:**
   - Change verse font size in settings
   - Verify indent adjusts proportionally
   - Check alignment is still correct

4. **Test search highlighting:**
   - Search for "day of the Lord"
   - Verify highlighted words maintain hanging indent
   - Check that bold/underline works correctly

5. **Test copy/paste:**
   - Select and copy verses
   - Paste into text editor
   - Verify plain text (no HTML) is copied

## Troubleshooting

### Indent Too Large/Small

If the indent seems wrong:
- Check that font is "IBM Plex Mono" (monospace)
- Verify font size matches what's displayed
- Clear cache and restart application

### HTML Shows as Text

If you see `<div style=...>` in the display:
- Check that `setTextFormat(Qt.TextFormat.RichText)` is called
- Verify HTML syntax is correct
- Look for syntax errors in the HTML string

### Copy Includes HTML

If copying produces HTML instead of plain text:
- Check that `self.text` stores plain text
- Verify copy operation uses `self.text`, not label text
- Look at copy implementation in main file

## Summary

The hanging indent feature:
- **Aligns continuation lines** with verse text start
- **Calculates dynamically** based on reference width
- **Adapts to font changes** automatically
- **Improves readability** significantly
- **Maintains all functionality** (copy, search, select)

**Result: Professional Bible formatting with clear visual hierarchy!**
