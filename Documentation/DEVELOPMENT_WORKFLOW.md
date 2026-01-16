# Bible Search Lite - Development Workflow

## Quick Reference Guide

### Daily Development Cycle

```
┌─────────────────────────────────────────────────────┐
│  1. DEVELOP                                         │
│     - Edit code in your IDE                         │
│     - Test changes                                  │
│     - Run bible_search_lite.py to verify            │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  2. COMMIT (using dev_manager.py)                   │
│     - Open dev_manager.py                           │
│     - Tab: 📝 Commits                               │
│     - Stage All Changes                             │
│     - Write commit message                          │
│     - Click "Commit"                                │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  3. PUSH TO GITHUB                                  │
│     - Click "Push to GitHub"                        │
│     - Now your code is backed up online             │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  4. REPEAT                                          │
│     - Go back to step 1                             │
│     - Do this many times (multiple commits)         │
└─────────────────────────────────────────────────────┘
```

### Release Cycle (When Ready for Users)

```
┌─────────────────────────────────────────────────────┐
│  1. PREPARE FOR RELEASE                             │
│     - Make sure all commits are pushed              │
│     - Test everything thoroughly                    │
│     - Update documentation if needed                │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  2. CREATE RELEASE (using dev_manager.py)           │
│     - Tab: 🚀 Releases                              │
│     - Enter version (e.g., v1.0.6)                  │
│     - Write release notes                           │
│     - Click "Create Release on GitHub"              │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  3. UPLOAD FILES (on GitHub.com)                    │
│     - Go to GitHub → Releases                       │
│     - Find your new tag                             │
│     - Click "Create release from tag"               │
│     - Upload: bible_data.sql.gz, checksums.txt      │
│     - Publish release                               │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  4. ANNOUNCE                                        │
│     - Users can now download this version           │
│     - Update any installation instructions          │
└─────────────────────────────────────────────────────┘
```

## File Organization

### Your Repository Structure

```
bible-search-lite/
├── .git/                          (Git repository data - don't touch)
├── bible_search_lite.py           (Main application - USERS GET THIS)
├── bible_search.py                (Core search logic - USERS GET THIS)
├── bible_search_ui/               (UI components - USERS GET THIS)
├── database/
│   ├── bibles.db                  (Bible database - USERS GET THIS)
│   └── subjects.db                (User data - created by app)
├── dev_manager.py                 (THIS TOOL - DEVELOPERS ONLY)
├── DEV_MANAGER_GUIDE.md           (This guide - DEVELOPERS ONLY)
├── setup.py                       (Linux installer - USERS GET THIS)
├── setup_win11.py                 (Windows installer - USERS GET THIS)
├── VERSION.txt                    (Version number - USERS GET THIS)
└── README.md                      (Documentation - USERS GET THIS)
```

### What Users Download

When you create a release, users download:
- Application files (bible_search_lite.py, etc.)
- Database (bible_data.sql.gz)
- Installer (setup.py or setup_win11.py)
- Documentation (README.md)

They do NOT get:
- dev_manager.py
- DEV_MANAGER_GUIDE.md
- Your .git folder

## Git Concepts Visualized

### Commits = Save Points

```
Time ────────────────────────────────────────▶

Commit 1         Commit 2         Commit 3
"Fix bug"        "Add feature"    "Update docs"
    │                │                │
    ●────────────────●────────────────●  ← main branch
```

Each commit is a snapshot of your entire codebase at that moment.

### Tags = Version Labels

```
Commit 1    Commit 2    Commit 3    Commit 4    Commit 5
    │           │           │           │           │
    ●───────────●───────────●───────────●───────────●
                            │                       │
                         v1.0.4                  v1.0.5
                         (tag)                   (tag)
```

Tags mark specific commits as releases.

### Development vs Released

```
GITHUB
┌────────────────────────────────────────────────────┐
│  Commits (Development)                             │
│  ●───●───●───●───●───●───●                         │
│                  │       │                         │
│               v1.0.4  v1.0.5                       │
│                  │       │                         │
│  Releases (Users Download)                         │
│  📦 v1.0.4      📦 v1.0.5                          │
└────────────────────────────────────────────────────┘
```

Users only see the releases (📦).
Developers see all commits (●).

## Example Scenarios

### Scenario 1: Daily Bug Fix

```
Morning:
1. Find bug in search highlighting
2. Edit widgets.py to fix it
3. Test - it works!
4. Open dev_manager.py
5. Stage changes
6. Commit: "Fix highlighting bug"
7. Push to GitHub
✅ Done! Bug fix is now backed up on GitHub
```

### Scenario 2: Multiple Features

```
Week of development:
Monday:    Commit "Add regex support"      ─┐
Tuesday:   Commit "Improve performance"     │
Wednesday: Commit "Fix edge case"           ├─ Multiple commits
Thursday:  Commit "Add tests"               │
Friday:    Commit "Update documentation"   ─┘

Friday afternoon:
1. All commits pushed to GitHub ✓
2. Everything tested ✓
3. Ready for release!
4. Open dev_manager.py → Releases tab
5. Create v1.1.0 (minor version - new features)
6. Write release notes listing all changes
7. Upload database to GitHub release
8. Announce to users

✅ Done! Users can download v1.1.0
```

### Scenario 3: Emergency Hotfix

```
User reports critical bug:
1. Fix the bug immediately
2. Test thoroughly
3. Commit: "Fix critical database corruption bug"
4. Push to GitHub
5. Create v1.0.6 (patch version - bug fix)
6. Upload to GitHub releases
7. Notify users of urgent update

✅ Done! Critical fix deployed quickly
```

## Best Practices

### Commit Messages

❌ Bad:
```
"Fixed stuff"
"Update"
"Changes"
```

✅ Good:
```
"Fix mouse event handling in highlighted verses

- Added setTextInteractionFlags to prevent label from capturing clicks
- Ensures verse clicks properly trigger comment editor"
```

### Version Numbers

```
v1.0.4 → v1.0.5   Small bug fix
v1.0.5 → v1.1.0   New feature added
v1.9.0 → v2.0.0   Major rewrite
```

### Release Notes

✅ Good release notes:
```markdown
## What's New in v1.0.5

- ✨ Search term highlighting now preserves quoted phrases
- 🐛 Fixed comment functionality in Window 5
- ⚡ Improved search performance by 20%

## Bug Fixes

- Mouse clicks on highlighted verses now work correctly
- Phrase matching no longer splits on individual words

## Installation

Download and run setup_win11.py (Windows) or setup.py (Linux)
```

## Cheat Sheet

### Common Commands (via dev_manager.py)

| Task | Steps |
|------|-------|
| Save changes | Commits tab → Stage All → Commit → Push |
| Create release | Releases tab → Enter version → Write notes → Create |
| View history | History tab → See commits and releases |

### When to Create a Release

- ✅ After fixing critical bugs
- ✅ After adding significant features
- ✅ When users request a feature you've implemented
- ✅ On a regular schedule (e.g., monthly)
- ❌ After every single commit (too many releases!)
- ❌ When code isn't tested

### Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| "Not a git repository" | Run from bible-search-lite folder |
| Can't push | Check internet, configure git credentials |
| Tag exists | Use next version number |
| No changes to commit | Make sure you edited and saved files |

## Getting Help

1. **Read DEV_MANAGER_GUIDE.md** - Comprehensive guide
2. **Check this workflow** - Visual reference
3. **Git documentation** - https://git-scm.com/doc
4. **GitHub guides** - https://guides.github.com

---

**Remember:** The tool makes git easier, but understanding these concepts will make you a better developer!

**Next Steps:**
1. Read DEV_MANAGER_GUIDE.md for detailed instructions
2. Try creating a test commit
3. Practice the workflow on non-critical changes
4. Create your first release when ready!
