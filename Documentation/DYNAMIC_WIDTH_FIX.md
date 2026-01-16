# Dynamic Width Fix - Removing Blank Spaces in Wide Windows

## Problem Identified

After removing the blank lines between verses, there was still a **gap appearing after some long verses** (like Isa 2:19) when the window was opened wide.

**Root Cause:**
The `sizeHint()` method was using a **hardcoded width of 600px** to calculate verse heights, but the actual window width was much larger (~1300px in your screenshot).

```python
# OLD CODE - BROKEN
default_width = 600  # ← HARDCODED!
text_width = default_width - 16 - 5 - 3 - 3  # = 573px
```

**What was happening:**
1. Window is 1300px wide
2. sizeHint calculates height assuming 600px width
3. At 600px, verse 2:19 wraps to 3 lines → needs 45px height
4. At 1300px, verse 2:19 only wraps to 2 lines → only needs 25px height
5. Result: **20px of blank space** because widget is too tall

## Visual Example

```
At 600px width (what sizeHint assumed):
┌────────────────────────────────────────────┐
│ KJV Isa 2:19 - And they shall go into the │
│ holes of the rocks, and into the caves of  │
│ the earth, for fear...                     │
└────────────────────────────────────────────┘
Height = 45px (3 lines)

At 1300px width (actual window size):
┌───────────────────────────────────────────────────────────────────────────────────────┐
│ KJV Isa 2:19 - And they shall go into the holes of the rocks, and into the caves of  │
│ the earth, for fear of the Lord, and for the glory of his majesty, when he ariseth...│
└───────────────────────────────────────────────────────────────────────────────────────┘
Height = 25px (2 lines)

But widget was allocated 45px → 20px blank space!
```

## Solution Implemented

### 1. Dynamic Width Detection

Updated `sizeHint()` to get the **actual list widget width** instead of using a hardcoded value:

```python
# NEW CODE - FIXED
actual_width = 600  # Fallback default

# Walk up the widget tree to find the list widget
parent = self.parent()
while parent:
    if hasattr(parent, 'viewport'):
        # Found the list widget - get its actual viewport width
        actual_width = parent.viewport().width()
        break
    parent = parent.parent() if hasattr(parent, 'parent') else None

# Calculate text width based on ACTUAL window width
text_width = actual_width - 16 - 5 - 3 - 3 - 20  # Account for scrollbar
```

### 2. Resize Event Handler

Added `resizeEvent()` to recalculate verse heights when the window is resized:

```python
def resizeEvent(self, event):
    """
    Handle resize events to recalculate verse heights based on new width.
    
    When the window is resized, text wrapping changes, so we need to
    recalculate the height of each verse item to match the new width.
    """
    super().resizeEvent(event)
    
    # Update all item sizes to match new width
    if hasattr(self, 'verse_items') and self.verse_items:
        self.update_item_sizes()
```

## Changes Made to widgets.py

### Location 1: `sizeHint()` method (Lines 192-244)

**Before:**
```python
default_width = 600
text_width = default_width - 16 - 5 - 3 - 3
```

**After:**
```python
# Try to get the actual width from the list widget
actual_width = 600  # Fallback default

# Walk up the widget tree to find the list widget
parent = self.parent()
while parent:
    if hasattr(parent, 'viewport'):
        actual_width = parent.viewport().width()
        break
    parent = parent.parent() if hasattr(parent, 'parent') else None

# Calculate text width based on actual width
text_width = actual_width - 16 - 5 - 3 - 3 - 20
text_width = max(text_width, 400)  # Ensure reasonable minimum
```

### Location 2: Added `resizeEvent()` method (Lines 742-759)

```python
def resizeEvent(self, event):
    """Handle resize events to recalculate verse heights"""
    super().resizeEvent(event)
    
    if hasattr(self, 'verse_items') and self.verse_items:
        self.update_item_sizes()
```

## Expected Results

After applying this fix:

✅ **No blank spaces** - Verses use correct height for actual window width
✅ **Adapts to window size** - Heights recalculate when you resize the window
✅ **Works at any width** - From narrow (600px) to ultra-wide (2000px+)
✅ **No performance issues** - Only recalculates on resize, not continuously

## How It Works

### Initial Display:
1. User searches for verses
2. Verses are added to list
3. `sizeHint()` gets actual list widget width
4. Calculates correct height for each verse
5. No blank spaces!

### Window Resize:
1. User drags window to make it wider/narrower
2. `resizeEvent()` is triggered
3. Calls `update_item_sizes()`
4. Each verse recalculates its height for new width
5. Text reflows properly, no blank spaces!

### Text Wrapping Example:

**Narrow window (600px):**
```
Verse wraps to 3 lines
Height = 45px
```

**Medium window (900px):**
```
Verse wraps to 2 lines
Height = 30px
```

**Wide window (1300px):**
```
Verse wraps to 2 lines (longer lines)
Height = 25px
```

**Each width gets the EXACT height needed!**

## Installation

1. **Backup current file:**
   ```bash
   cd ~/projects/bible-search-lite
   cp bible_search_ui/ui/widgets.py bible_search_ui/ui/widgets.py.backup3
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

1. **Test at narrow width:**
   - Resize window to be narrow (~600px wide)
   - Search for "Isa 2:12-22"
   - Verify no blank spaces between verses

2. **Test at wide width:**
   - Maximize window or make it very wide
   - Search for "Isa 2:12-22"
   - Verify no blank spaces (especially after verse 2:19)

3. **Test window resizing:**
   - Search for verses
   - Slowly resize window from narrow to wide
   - Watch verses reflow smoothly
   - Verify no blank spaces at any width

4. **Test with very long verses:**
   - Search for verses like Esther 8:9 (very long)
   - Resize window
   - Verify proper height adjustment

## Technical Details

### Why the Parent Walk?

```python
parent = self.parent()
while parent:
    if hasattr(parent, 'viewport'):
        actual_width = parent.viewport().width()
        break
    parent = parent.parent()
```

- `VerseItemWidget` doesn't know the list width directly
- We walk up the widget hierarchy to find the `QListWidget`
- QListWidget has a `viewport()` that gives us the actual display width
- This accounts for scrollbars, borders, and actual available space

### Why Subtract 20px?

```python
text_width = actual_width - 16 - 5 - 3 - 3 - 20
```

- 16px: Checkbox width
- 5px: Spacing between checkbox and text
- 3px: Left margin
- 3px: Right margin
- 20px: Scrollbar width (approximate)
- **Total**: Ensures we don't overestimate available text width

### Performance Impact

**Minimal:**
- `sizeHint()` called only when adding verses or resizing
- Not called during scrolling (Qt caches size hints)
- Parent walk is fast (typically only 2-3 levels)
- Resize only triggers when user actually resizes window

## Summary

**The blank space problem was caused by using a hardcoded width instead of the actual window width.**

The fix:
1. Dynamically detects the real list widget width
2. Calculates verse heights based on actual available space
3. Recalculates when window is resized
4. Results in perfect spacing at any window width

**No more blank spaces, regardless of window size!**
