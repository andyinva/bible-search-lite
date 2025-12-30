# Migration Plan: Remove user_data.db Dependency

## Overview
Remove the deprecated `UserDataService` and `user_data.db`, consolidating all subject/verse management into the newer `subjects.db` system managed by `SubjectManager`.

## Current State Analysis

### Two Overlapping Systems
1. **Old System (TO BE REMOVED)**:
   - Database: `database/user_data.db`
   - Service: `services/user_data_service.py` and `bible_search_ui/services/user_data_service.py`
   - Schema: groups → subjects → verses → comments (hierarchical)
   - Used in: Old deprecated UI components in `bible_search_lite.py`

2. **New System (KEEP)**:
   - Database: `database/subjects.db`
   - Manager: `subject_manager.py`, `subject_verse_manager.py`, `subject_comment_manager.py`
   - Schema: subjects → verses (simpler, flat)
   - Used in: Windows 4 & 5 (modular, toggleable UI)

### Key Difference
The old system has a **Groups** concept (groups contain subjects). The new system has only **Subjects** (no groups).

**Decision**: Remove the Groups hierarchy. Users who need organization can use naming conventions (e.g., "NT-Prayer", "OT-Prayer").

## Files to Modify

### 1. `bible_search_lite.py` (Main file - 15 changes needed)
**Lines to remove/change:**
- Line 10: Remove `from services.user_data_service import UserDataService`
- Line 143: Remove `self.user_data_service = UserDataService('database/user_data.db')`
- Lines 144-145: Remove `self.current_group_id` and `self.current_subject_id` (already tracked in subject_manager)
- Line 160: Remove `self.load_groups()` call
- Lines 585-658: Remove `create_subject_controls()` method (deprecated)
- Lines 1607-1652: Replace `on_acquire_verses_to_subject()` - use subject_manager instead
- Lines 1655-1688: Remove `on_group_changed()` method
- Lines 1689-1713: Remove `on_subject_changed()` method
- Lines 1750-1795: Replace `on_delete_verses()` - use subject_manager instead
- Lines 1776-1840: Replace `load_subject_verses()` - use subject_manager instead
- Lines 3268-3290: Remove `on_new_group()` method
- Lines 3292-3327: Remove `on_new_subject()` method
- Lines 3330-3365: Remove `on_delete_group()` method
- Lines 3367-3406: Remove `on_delete_subject()` method
- Lines 3541-3568: Remove `load_groups()` method

**Components that reference groups/subjects (TO BE REMOVED):**
- `self.group_combo` - Group dropdown
- `self.subject_combo` - Subject dropdown
- New Group/Delete Group buttons
- New Subject/Delete Subject buttons

These are **deprecated** - the new SubjectManager (Windows 4 & 5) already provides this functionality.

### 2. Files to DELETE
- `services/user_data_service.py`
- `bible_search_ui/services/user_data_service.py`
- `bible_search_ui/services/__init__.py` (references UserDataService)
- `bible_search_ui/controllers/user_data_controller.py` (uses UserDataService)
- `bible_search_ui/controllers/__init__.py` (if it only exports user_data_controller)

### 3. `.gitignore`
- Keep `database/subjects.db` (user-specific)
- Keep `database/user_data.db` (in case users have old data - they can migrate manually if needed)

### 4. `README.md`
- Update architecture diagram
- Remove references to UserDataService
- Update database documentation to show only `subjects.db`
- Remove `user_data.db` from database section

## Migration Strategy

### Phase 1: Remove Old UI Components
1. Remove group/subject dropdowns and related buttons from main window
2. Remove event handlers (on_group_changed, on_subject_changed, etc.)
3. Remove `self.current_group_id` and `self.current_subject_id` state variables

### Phase 2: Route Operations to SubjectManager
The new `subject_manager.verse_manager` already has all the functionality:
- Create subject: `subject_verse_manager.on_create_subject()`
- Load subjects: `subject_verse_manager.load_subjects()`
- Add verses: `subject_verse_manager.add_verses()`
- Delete verses: `subject_verse_manager.on_delete_verses()`
- Delete subject: `subject_verse_manager.on_delete_subject()`

No code rewrite needed - just **remove** the old code paths.

### Phase 3: Update Window 3 (Reading Window)
Window 3 has a "Send" button that currently tries to add verses to subjects. This should:
- Use `self.subject_manager.verse_manager` methods
- Reference subjects by name from `subjects.db` (no groups)

Currently at lines 4026-4137, the code already uses `subject_manager.db_conn` directly!
Just need to clean up any UserDataService references.

### Phase 4: Clean Up Imports and Files
1. Delete deprecated service files
2. Remove imports
3. Update documentation

## Testing Plan

After migration:
1. Test creating a new subject (Window 4)
2. Test adding verses to subject from Window 2 (Search)
3. Test adding verses from Window 3 (Reading) via "Send" button
4. Test deleting verses from subject
5. Test renaming subject
6. Test deleting subject
7. Verify database persistence (close/reopen app)

## User Impact

**Breaking Change**: Users with existing `user_data.db` data will lose access to it.

**Migration Path** (optional - for users who want to keep their data):
- Provide a separate migration script that:
  1. Reads groups/subjects/verses from `user_data.db`
  2. Flattens the hierarchy (combines group+subject names like "NT-Prayer")
  3. Writes to `subjects.db`

**Recommendation**: Don't provide migration - this is alpha software and the new system is cleaner.

## Implementation Order

1. **Remove old UI** (group/subject dropdowns, buttons)
2. **Remove old event handlers** (on_group_changed, etc.)
3. **Remove UserDataService import and initialization**
4. **Remove state variables** (current_group_id, current_subject_id)
5. **Delete service files**
6. **Update README**
7. **Test thoroughly**
8. **Commit with clear message about breaking change**

## Risks

**Low Risk** - The new system is already fully functional and in use. We're just removing dead code that runs in parallel.

**No Data Loss Risk** - We're keeping `user_data.db` in gitignore, just not using it in code. Users' existing data won't be deleted.
