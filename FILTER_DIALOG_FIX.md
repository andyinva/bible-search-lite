# Filter Dialog Performance Fix

## Issues Addressed

### Issue 1: Unnecessary Delay When Closing Filter Dialog

When opening the Filter dialog just to view word variations and then closing it (via "Close" button or X), users experienced a delay of several seconds before other buttons in Window 2 became responsive again.

**Root Cause:** The "Close" button was calling `self.accept()`, which returns `True` from the dialog. This caused the `show_filter_dialog()` method to execute filter update code (lines 1821-1834) even though the user hadn't made any changes - they just wanted to view the variations.

### Issue 2: No Feedback During Word Extraction

When clicking the Filter button, there was no indication that the system was analyzing word variations. For large search results, this could take several seconds with no feedback to the user.

### Issue 3: Clicking Filter Button While Dialog Is Open Causes Hang

When the Filter dialog was already open and the user clicked the Filter button again, it would trigger the word extraction process again, causing a long hang before anything happened. This was confusing and frustrating.

### Issue 4: Delay When Reopening Filter Dialog (After Closing)

After closing the Filter dialog and clicking the Filter button again (without doing a new search), the system would re-extract word variations, causing the same delay every time. This made the toggle behavior (open/close/open/close) frustrating because only the first close was fast - reopening always had a delay.

### Code Flow (Before Fix)

```
User clicks "Close" or X
  ↓
Dialog calls self.accept()
  ↓
dialog.exec() returns True
  ↓
show_filter_dialog() processes lines 1821-1834:
  - Get selected words
  - Store filtered words
  - Update filter button state
  - Display message
  ↓
Unnecessary processing causes delay
```

## Solutions

### Fix 1: Change Close Button Behavior

Changed the "Close" button to call `self.reject()` instead of `self.accept()`. This makes the dialog return `False` when closed without applying changes.

### Fix 2: Add "Analyzing..." Progress Indicator

Added a message that displays "Analyzing word variations..." while the `extract_word_counts()` method processes the search results. This provides immediate feedback to the user.

### Fix 3: Toggle Behavior for Filter Button

Added toggle behavior: if the Filter dialog is already open and the user clicks the Filter button again, it simply closes the dialog (same as clicking Close or X). This prevents the hang and provides intuitive UX.

### Fix 4: Cache Word Counts for Instant Reopening

Added caching mechanism for word counts. After the first extraction, the results are cached and reused when reopening the dialog (until a new search is performed). This makes the open/close/open sequence instant.

### Code Flow (After Fix)

**Scenario 1: User just wants to view variations**
```
User clicks "Close" or X
  ↓
Dialog calls self.reject()
  ↓
dialog.exec() returns False
  ↓
show_filter_dialog() skips lines 1821-1834
  ↓
No processing, no delay ✓
```

**Scenario 2: User applies filter**
```
User clicks "Search" button
  ↓
Dialog calls search_and_close():
  - Stores filtered words
  - Updates filter button
  - Triggers search immediately
  - Calls self.accept()
  ↓
dialog.exec() returns True
  ↓
Filter already applied ✓
```

**Scenario 3: User clicks Filter button while dialog is open (NEW)**
```
User clicks "Filter" button (dialog already visible)
  ↓
show_filter_dialog() checks: is filter_dialog visible?
  ↓
Yes → Call filter_dialog.reject() and return immediately
  ↓
Dialog closes instantly
  ↓
No word extraction, no processing, no delay ✓
```

**Scenario 4: User reopens filter dialog after closing (NEW)**
```
User clicks "Filter" button (after previously closing dialog)
  ↓
show_filter_dialog() checks: is _cached_word_counts available?
  ↓
Yes → Use cached word counts (instant, no extraction)
  ↓
Dialog opens immediately with cached data
  ↓
No delay ✓

---

User performs new search
  ↓
perform_search() clears _cached_word_counts
  ↓
Next Filter click will extract fresh word counts
```

## Files Changed

### 1. [bible_search_ui/ui/dialogs.py:901](bible_search_ui/ui/dialogs.py#L901)

**Change:** Close button now calls `reject()` instead of `accept()`

```python
# Before:
close_btn.clicked.connect(self.accept)

# After:
close_btn.clicked.connect(self.reject)
```

### 2. [bible_search_lite.py:1792-1863](bible_search_lite.py#L1792-L1863) - show_filter_dialog()

**Changes:**
- Added toggle behavior to close dialog if Filter button clicked while open
- Added caching for word counts to avoid re-extraction
- Added progress message during word extraction
- Store dialog reference for toggle functionality

```python
# Added at start of show_filter_dialog():
# If the filter dialog is already open, close it (toggle behavior)
if hasattr(self, 'filter_dialog') and self.filter_dialog and self.filter_dialog.isVisible():
    self.debug_print("📦 Filter dialog already open - closing it")
    self.filter_dialog.reject()  # Close as if user clicked Close/X
    return

# ... validation checks ...

# Check cache first (instant reopening):
if hasattr(self, '_cached_word_counts') and self._cached_word_counts:
    self.debug_print("📦 Using cached word counts (instant)")
    word_counts = self._cached_word_counts
else:
    # Show "Analyzing..." message while extracting
    self.set_message("Analyzing word variations...")
    QApplication.processEvents()  # Force UI update

    # Extract word counts from current search results
    word_counts = self.extract_word_counts()

    # Cache for fast reopening
    self._cached_word_counts = word_counts
    self.debug_print("💾 Cached word counts for fast reopening")

    # Clear the message
    self.set_message("")

# Store dialog reference:
self.filter_dialog = SearchFilterDialog(self, word_counts)
if self.filter_dialog.exec():
    # ... process results ...

# Clear reference when dialog closes:
self.filter_dialog = None
```

### 3. [bible_search_lite.py:2386-2395](bible_search_lite.py#L2386-L2395) - perform_search()

**Change:** Clear word counts cache when new search is performed

```python
# Record search start time and search query
self.search_start_time = time.time()
self.current_search_query = search_term

# Clear cached word counts since we're doing a new search
self._cached_word_counts = None
self.debug_print("🗑️  Cleared word counts cache for new search")
```

## Testing

### Test 1: No Delay When Closing Without Changes

1. Open Bible Search Lite
2. Perform a wildcard search (e.g., "send*")
3. Click the "Filter" button
4. **DO NOT change any checkboxes**
5. Click "Close" or the X
6. Try clicking other buttons immediately

**Expected Result:** Buttons should be responsive immediately with no delay.

### Test 2: Progress Message Displays

1. Open Bible Search Lite
2. Perform a large wildcard search (e.g., "send*" or "love*")
3. Click the "Filter" button
4. Observe the message area (Window 1, bottom)

**Expected Result:** You should briefly see "Analyzing word variations..." message before the filter dialog opens.

### Test 3: Toggle Behavior (Close on Second Click)

1. Open Bible Search Lite
2. Perform any search (e.g., "love")
3. Click the "Filter" button to open the dialog
4. **Click the "Filter" button again** (while dialog is still open)

**Expected Result:** The dialog should close immediately, just like clicking the Close or X button. No hang, no delay.

### Test 4: Fast Reopening (Cache Test)

1. Open Bible Search Lite
2. Perform a wildcard search (e.g., "send*")
3. Click the "Filter" button → dialog opens (shows "Analyzing..." briefly on first time)
4. Close the dialog (click Close or X)
5. **Click the "Filter" button again**
6. Close and reopen several times

**Expected Result:**
- First open: Shows "Analyzing..." message briefly
- Subsequent opens: Opens instantly with no delay (uses cache)
- After new search: Will show "Analyzing..." again for the new results

## Benefits

### Fix 1: Close Button Change
- **Faster UI response:** No unnecessary processing when just viewing variations
- **Better user experience:** User can quickly check variations without waiting
- **Logical behavior:** Close = cancel (no changes), Search = apply (with changes)
- **Follows Qt conventions:** `accept()` for OK/Apply, `reject()` for Cancel/Close

### Fix 2: Progress Indicator
- **User awareness:** Users know the system is working when extraction takes time
- **Professional feedback:** No more wondering if the button click registered
- **Reduces perceived wait time:** Visual feedback makes waiting feel shorter
- **Minimal overhead:** Message display is nearly instant, adds no significant delay

### Fix 3: Toggle Behavior
- **Prevents hang:** No more waiting when clicking Filter button while dialog is open
- **Intuitive UX:** Common pattern where clicking the same button closes what it opened
- **Fast response:** Dialog closes immediately without processing
- **Consistent behavior:** Works just like clicking Close or X button

### Fix 4: Caching Mechanism
- **Instant reopening:** After first extraction, reopening the dialog is instant
- **Smart invalidation:** Cache is cleared automatically when you perform a new search
- **Memory efficient:** Stores only word counts dictionary, not full verse data
- **Transparent:** Works automatically without user intervention
- **Perfect for exploring:** Can open/close/open the filter dialog rapidly without delays
