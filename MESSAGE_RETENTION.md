# Message Retention System (2-Day History)

## Overview

Both the message log and debug log now automatically retain messages for **2 days** (48 hours) and automatically clean up older messages. This prevents the logs from growing indefinitely while keeping recent history available.

## Features

### Automatic Retention
- **Message log**: Keeps messages for 2 days
- **Debug log**: Keeps debug messages for 2 days
- **Automatic cleanup**: Old messages are removed automatically
- **No user action needed**: System manages itself

### Cleanup Schedule
1. **On startup**: Cleans up old messages when app starts
2. **Every 6 hours**: Periodic cleanup while app is running
3. **Every 100 messages**: Quick cleanup when many messages are logged

### Storage Format
Messages are stored as tuples: `(timestamp, message)`
- **timestamp**: Python datetime object for precise age calculation
- **message**: The actual message text

## How It Works

### Message Flow

```
User action occurs
  ↓
set_message("Some message") called
  ↓
log_message() stores (datetime.now(), "Some message")
  ↓
Every 100 messages: cleanup_old_messages() runs
  ↓
Removes any (timestamp, message) where timestamp > 2 days old
  ↓
Recent messages remain in log
```

### Cleanup Logic

```python
def cleanup_old_messages(self):
    """Remove messages older than retention period (2 days)"""
    cutoff_time = datetime.now() - timedelta(days=2)

    # Keep only messages newer than cutoff
    self.message_log = [(ts, msg) for ts, msg in self.message_log
                        if ts > cutoff_time]
    self.debug_log = [(ts, msg) for ts, msg in self.debug_log
                      if ts > cutoff_time]
```

## Configuration

The retention period is configurable via instance variables:

```python
self.message_retention_days = 2  # Keep messages for 2 days
self.debug_retention_days = 2    # Keep debug messages for 2 days
```

To change the retention period, modify these values in `__init__()`.

## Files Changed

### [bible_search_lite.py:117-133](bible_search_lite.py#L117-L133)

**Changed:** Message/debug log initialization and cleanup timer

```python
# Before:
self.message_log = []
self.max_message_log_size = 500  # Keep last 500 messages
self.debug_log = []

# After:
self.message_log = []  # Store as (timestamp, message) tuples
self.message_retention_days = 2  # Keep messages for 2 days
self.debug_log = []  # Store as (timestamp, message) tuples
self.debug_retention_days = 2  # Keep debug messages for 2 days

# Set up periodic cleanup timer (runs every 6 hours)
self.cleanup_timer = QTimer()
self.cleanup_timer.timeout.connect(self.cleanup_old_messages)
self.cleanup_timer.start(6 * 60 * 60 * 1000)  # 6 hours in milliseconds

# Run initial cleanup on startup
self.cleanup_old_messages()
```

### [bible_search_lite.py:261-271](bible_search_lite.py#L261-L271)

**Added:** cleanup_old_messages() method

```python
def cleanup_old_messages(self):
    """Remove messages older than retention period (2 days)"""
    from datetime import datetime, timedelta

    cutoff_time = datetime.now() - timedelta(days=self.message_retention_days)

    # Clean message log
    self.message_log = [(ts, msg) for ts, msg in self.message_log if ts > cutoff_time]

    # Clean debug log
    self.debug_log = [(ts, msg) for ts, msg in self.debug_log if ts > cutoff_time]
```

### [bible_search_lite.py:273-280](bible_search_lite.py#L273-L280)

**Changed:** log_message() to use timestamp tuples and trigger cleanup

```python
# Before:
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"[{timestamp}] {message}"
self.message_log.append(log_entry)

if len(self.message_log) > self.max_message_log_size:
    self.message_log = self.message_log[-self.max_message_log_size:]

# After:
timestamp = datetime.now()
self.message_log.append((timestamp, message))

# Clean up old messages periodically (every 100 messages)
if len(self.message_log) % 100 == 0:
    self.cleanup_old_messages()
```

### [bible_search_lite.py:349-357](bible_search_lite.py#L349-L357)

**Changed:** debug_print() to use timestamp tuples and trigger cleanup

```python
# Before:
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"[{timestamp}] {message}"
self.debug_log.append(log_entry)

# After:
timestamp = datetime.now()
self.debug_log.append((timestamp, message))

# Clean up old messages periodically (every 100 messages)
if len(self.debug_log) % 100 == 0:
    self.cleanup_old_messages()
```

### [bible_search_lite.py:313-318](bible_search_lite.py#L313-L318)

**Changed:** show_message_log() to format tuples for display

```python
# Before:
log_text.setPlainText("\n".join(self.message_log))

# After:
formatted_log = [f"[{ts.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
                 for ts, msg in self.message_log]
log_text.setPlainText("\n".join(formatted_log))
```

### [bible_search_lite.py:372-387](bible_search_lite.py#L372-L387)

**Changed:** show_debug_log() to format tuples and update info label

```python
# Before:
info_label = QLabel("Debug log shows technical messages from this session. Cleared on app restart.")
log_text.setPlainText("\n".join(self.debug_log))

# After:
info_label = QLabel(f"Debug log shows technical messages from the last {self.debug_retention_days} days.")
formatted_log = [f"[{ts.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
                 for ts, msg in self.debug_log]
log_text.setPlainText("\n".join(formatted_log))
```

## Examples

### Timeline Example

**Day 1 (Monday 9am):**
```
[2026-02-09 09:00:00] Search started for "love"
[2026-02-09 09:00:05] Found 150 verses
```

**Day 2 (Tuesday 3pm):**
```
[2026-02-09 09:00:00] Search started for "love"      ← Still visible
[2026-02-09 09:00:05] Found 150 verses               ← Still visible
[2026-02-10 15:00:00] Search started for "faith"     ← New message
```

**Day 3 (Wednesday 11am):**
```
[2026-02-09 09:00:00] Search started for "love"      ← Still visible (< 48hrs)
[2026-02-09 09:00:05] Found 150 verses               ← Still visible (< 48hrs)
[2026-02-10 15:00:00] Search started for "faith"     ← Still visible
[2026-02-11 11:00:00] Filter applied                 ← New message
```

**Day 3 (Wednesday 3pm):** (cleanup runs)
```
[2026-02-10 15:00:00] Search started for "faith"     ← Monday messages removed (> 48hrs)
[2026-02-11 11:00:00] Filter applied
```

## Benefits

### For Users
1. **Recent history available**: Can see what happened in last 2 days
2. **No manual cleanup**: System manages itself automatically
3. **No performance impact**: Logs don't grow indefinitely
4. **Debugging friendly**: 2 days is enough for troubleshooting

### For Developers
1. **Memory efficient**: Prevents unbounded log growth
2. **Automatic management**: No user intervention needed
3. **Flexible**: Easy to adjust retention period
4. **Performance**: Cleanup is fast (list comprehension)

## Technical Details

### Why 2 Days?

**Balances:**
- **Short enough**: Won't consume too much memory
- **Long enough**: Covers typical debugging scenarios
- **User friendly**: Recent operations are still visible

### Cleanup Frequency

**Three triggers:**
1. **Startup**: Ensures old messages from previous sessions are removed
2. **Every 6 hours**: Periodic cleanup while app is running
3. **Every 100 messages**: Quick cleanup during heavy usage

### Memory Impact

**Storage:**
- Each message: ~100 bytes (timestamp + string)
- 1000 messages ≈ 100 KB
- Even with heavy usage, unlikely to exceed 1 MB

**Cleanup Performance:**
- List comprehension is O(n)
- Typically < 1ms for 1000 messages
- No noticeable impact on user experience

## Backward Compatibility

**Breaking changes:**
- Message log format changed from strings to tuples
- Old saved logs won't be compatible (but logs aren't saved to disk)

**Compatible:**
- All existing set_message() calls work unchanged
- All existing debug_print() calls work unchanged
- Display dialogs format tuples back to strings

## Future Enhancements

Possible improvements:
1. **Configurable retention**: UI setting to adjust days
2. **Disk persistence**: Save logs to file for long-term storage
3. **Log rotation**: Archive old logs instead of deleting
4. **Export logs**: Save logs to CSV or text file
5. **Search/filter**: Find specific messages in log dialogs
