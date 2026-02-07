# Bible Search Lite - Release Wizard User Guide

## Overview

The **Release Wizard** is a comprehensive step-by-step GUI tool that guides you through the entire process of creating and publishing a release for Bible Search Lite. It automates file updates, database export, git operations, and GitHub release creation.

## Features

✅ **10-Step Guided Workflow** - Sequential steps you can't skip
✅ **Automated File Updates** - Updates VERSION.txt, setup.py, setup_win11.py
✅ **Database Export** - Runs export_bible_data.py automatically  
✅ **Git Integration** - Commit, tag, and push operations
✅ **GitHub Release Creation** - Creates releases and uploads files via GitHub CLI
✅ **Visual Progress Tracking** - Color-coded step navigation
✅ **Built-in Authentication** - Checks GitHub CLI on startup
✅ **Detailed Instructions** - Each step has clear guidance

## Installation

### Requirements

```bash
# Python 3.7+ with PyQt6
pip install PyQt6

# Git (usually pre-installed)
git --version

# GitHub CLI (for Step 9: GitHub Release)
gh --version

# If gh not installed:
# Ubuntu/Debian:
sudo apt install gh

# Or download from:
# https://cli.github.com/
```

### Setup

```bash
# Navigate to your project directory
cd /home/ajhinva/projects/bible-search-lite

# Make wizard executable
chmod +x release_wizard.py

# Run the wizard
python3 release_wizard.py
```

## User Interface

### Layout

The wizard uses a three-panel layout:

```
┌─────────────────────────────────────────────────────────┐
│ [Header: Step Title and Description]                    │
├──────────────┬──────────────────────────────────────────┤
│  1. Version  │                                           │
│  2. Notes    │                                           │
│  3. Update   │     Content Area                          │
│  4. Export   │     (Current Step)                        │
│  5. Status   │                                           │
│  6. Commit   │                                           │
│  7. Tag      │                                           │
│  8. Push     │                                           │
│  9. Release  │                                           │
│ 10. Done     │                                           │
└──────────────┴──────────────────────────────────────────┘
  Left Panel      Center Content Area
  (Steps)         (Instructions & Actions)
```

### Navigation

- **Left Panel**: Shows all 10 steps with color-coded status
  - **Gray**: Not yet reached
  - **Blue**: Current step
  - **Green border**: Completed steps
  
- **Auto-Advance**: Completing a step automatically moves to the next

- **Can't Skip**: Must complete steps in order

## Step-by-Step Guide

### Step 1: Version Number

**Purpose**: Set the version for this release

**Actions**:
1. View current version
2. Choose version bump:
   - **Major (x.0.0)**: Breaking changes
   - **Minor (0.x.0)**: New features
   - **Patch (0.0.x)**: Bug fixes
3. Or enter manually (e.g., v1.2.3)
4. Click "✓ Set Version and Continue"

**Tips**:
- Follow semantic versioning
- Always start versions with 'v'
- Format: v{major}.{minor}.{patch}

**Example**:
```
Current: v1.1.4
Click "Patch" → v1.1.5
Click "Minor" → v1.2.0
Click "Major" → v2.0.0
```

---

### Step 2: Release Notes

**Purpose**: Create release notes for GitHub

**Actions**:
1. Click "Generate Changelog" to auto-create from commits
2. Or write notes manually
3. Edit as needed
4. Click "✓ Save Notes and Continue"

**Tips**:
- Use Markdown formatting
- Include sections: What's New, Bug Fixes, Breaking Changes
- Mention database size and translation count
- Keep concise but informative

**Example**:
```markdown
## What's New
- Added two-color highlighting feature
- Enhanced wildcard search matching
- Improved apostrophe handling

## Bug Fixes
- Fixed phrase search in quoted strings
- Corrected filter re-highlighting behavior

## Database
- 39 Bible translations
- 31,102+ verses
- Compressed to 81 MB
```

---

### Step 3: Update Files

**Purpose**: Update version in all project files

**Actions**:
1. Click "🔄 Update All Files"
2. Wait for confirmation
3. Review status messages
4. Click "✓ Continue"

**Files Updated**:
- `VERSION.txt` → New version number
- `setup.py` → RELEASE_VERSION = "v1.2.3"
- `setup_win11.py` → RELEASE_VERSION = "v1.2.3"
- `bible_search_lite.py` → VERSION = "1.2.3" and window title date (e.g., "February 2026")

**What to Check**:
✅ All four files show success
✅ No error messages
✅ Status shows "All files updated successfully"

---

### Step 4: Export Database

**Purpose**: Create distribution files for GitHub Release

**Actions**:
1. Click "📦 Export Database"
2. Wait for export to complete (may take 30-60 seconds)
3. Verify files created
4. Click "✓ Continue"

**What It Does**:
- Runs `export_bible_data.py`
- Creates `data/bible_data.sql.gz` (~81 MB)
- Creates `data/checksums.txt` (SHA256 hash)

**Expected Output**:
```
Running export_bible_data.py...
✅ Export successful!

Created files:
  • bible_data.sql.gz (81.2 MB)
  • checksums.txt

Files are ready for GitHub Release upload.
```

---

### Step 5: Git Status

**Purpose**: Review changes before committing

**Actions**:
1. Review changed files list
2. Click "📎 Stage All Files"
3. Verify files are staged
4. Click "✓ Continue"

**What You'll See**:
```
M  VERSION.txt
M  setup.py
M  setup_win11.py
M  data/bible_data.sql.gz
M  data/checksums.txt
?? RELEASE_NOTES_v1.2.3.md
```

**Tips**:
- Check that expected files are listed
- Make sure no unwanted files are included
- Click "🔄 Refresh Status" to update view

---

### Step 6: Git Commit

**Purpose**: Create a git commit with your changes

**Actions**:
1. Click "Generate Commit Message" (auto-fills from version & notes)
2. Edit message if needed
3. Click "✅ Create Commit"
4. Wait for confirmation
5. Click "✓ Continue"

**Commit Message Format**:
```
Release v1.2.3: Enhanced search features

- Added two-color highlighting
- Improved wildcard matching
- Updated database with 39 translations
```

**Tips**:
- First line should be concise summary
- Include bullet points for details
- Mention database changes if relevant

---

### Step 7: Git Tag

**Purpose**: Create a version tag

**Actions**:
1. Verify version shown is correct
2. Click "🏷️  Create Tag"
3. If tag exists, confirm force update
4. Wait for confirmation
5. Click "✓ Continue"

**What It Does**:
- Creates annotated tag with version (e.g., v1.2.3)
- Attaches release notes to tag
- Prepares for GitHub push

**Handling Existing Tags**:
If tag already exists, you'll be asked:
```
Tag v1.2.3 already exists. Force update?
[Yes] [No]
```

Choose **Yes** to replace the tag.

---

### Step 8: Git Push

**Purpose**: Push commits and tags to GitHub

**Actions**:
1. Click "⬆️  Push Commits"
2. Wait for confirmation
3. Click "🏷️  Push Tags"
4. Wait for confirmation
5. Click "✓ Continue"

**Important**:
- Must push **both** commits and tags
- Both must succeed to continue
- If push fails, check internet connection

**Expected Output**:
```
Pushing commits to GitHub...
✅ Commits pushed successfully

Pushing tag v1.2.3 to GitHub...
✅ Tag v1.2.3 pushed successfully

✅ Everything pushed to GitHub!
```

---

### Step 9: GitHub Release

**Purpose**: Create GitHub Release and upload files

**Actions**:
1. Select release type:
   - **Latest** (production release)
   - **Pre-release** (beta/testing)
2. Verify files to upload are listed:
   - data/bible_data.sql.gz
   - data/checksums.txt
3. Click "🚀 Create GitHub Release"
4. Confirm creation
5. Wait for upload (may take 2-3 minutes)
6. Click "✓ Release Complete!"

**What It Does**:
- Creates GitHub Release from tag
- Uploads database file (81 MB)
- Uploads checksums file
- Sets release as Latest or Pre-release
- Provides release URL

**Requirements**:
- GitHub CLI must be installed
- Must be authenticated (`gh auth login`)
- Internet connection required

**Expected Output**:
```
Creating git tag...
Pushing tag to GitHub...
Creating GitHub release...
Uploading bible_data.sql.gz...
Uploading checksums.txt...
Release created successfully!

✅ Release v1.2.3 created successfully!

Uploaded 2 file(s).

🔗 Release URL: https://github.com/andyinva/bible-search-lite/releases/tag/v1.2.3
```

---

### Step 10: Complete

**Purpose**: Finalize and verify release

**Actions**:
1. Click "🌐 Open Release in Browser" to verify
2. Review release on GitHub
3. Test installation with setup.py
4. Click "✓ Close Wizard"

**What's Next**:
1. Visit GitHub release page
2. Verify all files are uploaded
3. Check release notes display correctly
4. Test installation on clean system
5. Announce release to users

**Release URL Format**:
```
https://github.com/andyinva/bible-search-lite/releases/tag/v1.2.3
```

---

## Troubleshooting

### Problem: "Not a git repository"

**Error**:
```
Not a git repository!
Please run this tool from the bible-search-lite directory.
```

**Solution**:
```bash
cd /home/ajhinva/projects/bible-search-lite
python3 release_wizard.py
```

---

### Problem: "GitHub CLI not authenticated"

**Error**:
```
GitHub CLI Not Authenticated
Not authenticated. Run: gh auth login
```

**Solution**:
```bash
# Authenticate with GitHub
gh auth login

# Choose:
# 1. GitHub.com
# 2. HTTPS protocol
# 3. Authenticate via browser

# Verify
gh auth status
```

---

### Problem: "Export failed"

**Error**:
```
❌ export_bible_data.py not found in current directory
```

**Solution**:
Make sure you're in the correct directory with export_bible_data.py:
```bash
ls export_bible_data.py
# Should exist

# If not found:
cd /home/ajhinva/projects/bible-search-lite
```

---

### Problem: "Push failed"

**Error**:
```
❌ Push failed: rejected
```

**Solution**:
```bash
# Pull latest changes first
git pull origin main

# Resolve any conflicts
git status

# Then try push again in wizard
```

---

### Problem: "Tag already exists"

**Error**:
```
Tag v1.2.3 already exists
```

**Solution**:
The wizard will ask if you want to force update. Choose **Yes** to replace the tag, or **No** to cancel and use a different version.

---

### Problem: "Release creation failed"

**Error**:
```
❌ Failed to create release: HTTP Error 422
```

**Solution**:
This usually means:
1. Tag wasn't pushed to GitHub
   - Go back to Step 8 and push tag
2. Release already exists
   - Delete old release on GitHub first
3. Network issue
   - Check internet connection

---

## Tips & Best Practices

### Before Starting

1. **Clean Working Directory**: Commit or stash unrelated changes
2. **Pull Latest**: Make sure you're up-to-date with remote
3. **Test Changes**: Verify your code works before releasing

### During Release

1. **Don't Close**: Complete all steps in one session
2. **Read Messages**: Pay attention to success/error messages
3. **Verify Each Step**: Check that each step succeeded before continuing

### After Release

1. **Test Installation**: Always test setup.py on clean system
2. **Check GitHub**: Verify files uploaded correctly
3. **Monitor Issues**: Watch for bug reports in first 24 hours

### Version Numbering

Follow semantic versioning strictly:
- **Major**: Breaking API changes (v2.0.0)
- **Minor**: New features, backward compatible (v1.3.0)
- **Patch**: Bug fixes only (v1.2.4)

### Release Notes Quality

Good release notes include:
- Clear feature descriptions
- Bug fix details
- Breaking changes (if any)
- Installation instructions
- Database statistics

---

## Comparison with Manual Process

### Manual Process (Old Way)

```bash
# 1. Update version files (manual editing)
vi VERSION.txt
vi setup.py
vi setup_win11.py
vi bible_search_lite.py  # Update VERSION and window title date

# 2. Create release notes (manual file)
vi RELEASE_NOTES_v1.2.3.md

# 3. Export database
python3 export_bible_data.py

# 4. Git operations
git add .
git commit -m "Release v1.2.3..."
git tag v1.2.3
git push origin main
git push origin v1.2.3

# 5. GitHub (website)
# - Go to releases page
# - Click "Create new release"
# - Select tag
# - Copy/paste notes
# - Upload files manually
# - Publish
```

**Time**: 15-20 minutes, error-prone

### Release Wizard (New Way)

```bash
python3 release_wizard.py
# Follow 10 guided steps
# Click buttons
# Done!
```

**Time**: 5-7 minutes, automated

---

## Features Summary

| Feature | Manual | Wizard |
|---------|--------|--------|
| Update VERSION.txt | ✋ Manual | ✅ Automatic |
| Update setup.py | ✋ Manual | ✅ Automatic |
| Update setup_win11.py | ✋ Manual | ✅ Automatic |
| Update bible_search_lite.py | ✋ Manual | ✅ Automatic |
| Export database | ✅ Script | ✅ Integrated |
| Create release notes | ✋ Manual | ✅ Generated |
| Git commit | ✋ Manual | ✅ Assisted |
| Git tag | ✋ Manual | ✅ Automatic |
| Git push | ✋ Manual | ✅ Automatic |
| GitHub release | ✋ Website | ✅ Automatic |
| Upload files | ✋ Website | ✅ Automatic |
| Progress tracking | ❌ None | ✅ Visual |
| Error checking | ❌ Manual | ✅ Built-in |
| Can't skip steps | ❌ Can skip | ✅ Enforced |

---

## Keyboard Shortcuts

While in the wizard:

- **Enter**: Click focused button
- **Tab**: Move between fields
- **Esc**: (none - must complete steps)

---

## Advanced Usage

### Customizing Release Notes

The wizard generates basic notes from git commits. For best results:

1. Use descriptive commit messages during development
2. Group related changes in single commits
3. Use conventional commit format:
   ```
   feat: Add two-color highlighting
   fix: Correct apostrophe handling
   docs: Update search operators guide
   ```

### Handling Large Files

The database file (81 MB) takes time to upload. The wizard shows:
- Progress messages
- Upload status for each file
- Final confirmation

Don't close the wizard during upload!

### Beta Releases

For pre-release versions:
1. Use version like v1.3.0-beta
2. Select "Pre-release" option in Step 9
3. GitHub will mark it as pre-release
4. Users won't see it as "Latest Release"

---

## Logging

The wizard displays all operations in real-time. To save logs:

### Method 1: Terminal Redirection
```bash
python3 release_wizard.py 2>&1 | tee release.log
```

### Method 2: Screenshot
Take screenshots of each step for your records.

---

## Support

If you encounter issues:

1. **Check this guide** - Most common problems are covered
2. **Verify requirements** - gh, git, PyQt6 installed
3. **Check GitHub** - Is github.com accessible?
4. **Test manually** - Try git commands in terminal

---

## Future Enhancements

Potential additions:

- [ ] Resume interrupted releases
- [ ] Rollback to previous step
- [ ] Save release template
- [ ] Email notification on completion
- [ ] Slack/Discord webhook integration
- [ ] Automated testing before release
- [ ] Changelog auto-formatting
- [ ] Multiple repository support

---

## Changelog

**Version 1.0** (February 2026)
- Initial release
- 10-step guided workflow
- Automated file updates
- GitHub CLI integration
- Database export integration
- Visual progress tracking

---

## Credits

**Author**: Andrew Hopkins
**Project**: Bible Search Lite
**Purpose**: Streamline release process

---

## License

This tool is part of the Bible Search Lite project.
Use freely for your releases!

---

**Last Updated**: February 3, 2026
**Compatible With**: Bible Search Lite v1.1.4+
