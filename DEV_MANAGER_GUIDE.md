# Development Manager Tool Guide

## What is This Tool?

`dev_manager.py` is a GUI tool for managing Bible Search Lite development. It helps you:
- View and create git commits
- Push changes to GitHub
- Create versioned releases for distribution
- See what's in development vs what's released

**⚠️ IMPORTANT:** This tool is for developers only. It is NOT included in Bible Search Lite distributions.

## Installation

No installation needed! Just make sure you have:
- Python 3.7+
- PyQt6 (`pip install PyQt6`)
- Git configured on your system

## Running the Tool

From the `bible-search-lite` directory:

```bash
python3 dev_manager.py
```

Or on Windows:

```bash
python dev_manager.py
```

## Understanding the Interface

### Tab 1: 📝 Commits

**Purpose:** Manage your day-to-day development work

**What You'll See:**
- Current branch (should usually be `main`)
- Uncommitted changes (files you've modified)
- Area to create commits

**How to Use:**
1. Make changes to your code
2. Click "🔄 Refresh Status" to see changed files
3. Click "📎 Stage All Changes" to prepare files for commit
4. Enter a commit message describing what you changed
5. Click "✅ Commit" to save the changes
6. Click "⬆️ Push to GitHub" to upload to GitHub

**Example Commit Message:**
```
Fix search highlighting bug

- Fixed phrase matching in quoted searches
- Improved performance of highlight rendering
```

### Tab 2: 🚀 Releases

**Purpose:** Create official versions for users to download

**What You'll See:**
- Current version number
- Form to create a new release

**How to Use:**

1. **Version Tag:** Enter version like `v1.0.5`
   - Use format: `v` + major.minor.patch
   - Examples: `v1.0.5`, `v1.1.0`, `v2.0.0`

2. **Release Notes:** Describe what's new
   ```markdown
   ## What's New
   - Added search term highlighting
   - Improved comment functionality

   ## Bug Fixes
   - Fixed mouse event handling
   - Fixed phrase matching in searches
   ```

3. **Release Type:**
   - **Latest** - Stable release for all users (most common)
   - **Pre-release** - Beta/testing version

4. Click "🚀 Create Release on GitHub"

5. **Next Steps** (shown in success message):
   - Go to GitHub.com → Your repository → Releases
   - Find your new tag
   - Click "Create release from tag"
   - Upload files (bible_data.sql.gz, checksums.txt)
   - Publish the release

### Tab 3: 📊 History

**Purpose:** See what's been committed and released

**What You'll See:**
- **Development Commits:** Recent changes not yet in a release
- **Released Versions:** All published versions with dates

**How to Use:**
- Review recent commits to see what's changed
- Check release history to see version progression
- Click "🔄 Refresh History" to update

## GitHub Concepts Explained

### Commits
Think of commits as "save points" in your development:
- You change code → Stage changes → Commit with message → Push to GitHub
- Each commit has a unique ID and message
- You can always go back to any commit

### Tags
Tags are labels on specific commits:
- Example: Tag `v1.0.5` points to a specific commit
- Tags mark "this is version 1.0.5 for users"
- Tags don't change (unlike branches)

### Releases
Releases are GitHub's way of packaging software for users:
- Based on tags (e.g., tag v1.0.5 → Release v1.0.5)
- Include release notes
- Can attach downloadable files (database, installers)
- Show up on the "Releases" page of your repo

### Workflow
```
1. Make code changes
2. Create commits (development)
3. Push commits to GitHub (backup/share)
4. When ready for users: Create release tag
5. Upload release files to GitHub release
6. Users download from Releases page
```

## Common Workflows

### Daily Development

1. Open `dev_manager.py`
2. Make code changes in your editor
3. Go to "📝 Commits" tab
4. Click "Refresh Status"
5. Review changed files
6. Click "Stage All Changes"
7. Write commit message
8. Click "Commit"
9. Click "Push to GitHub"

### Creating a New Version

1. Make sure all development commits are done
2. Go to "🚀 Releases" tab
3. Enter version (e.g., `v1.0.6`)
4. Write release notes describing changes
5. Select "Latest"
6. Click "Create Release on GitHub"
7. Follow instructions to upload files on GitHub

### Checking What's New

1. Go to "📊 History" tab
2. Look at "Development Commits" section
3. These are changes since last release
4. When you create a release, these become "released"

## Version Numbering Guide

Use semantic versioning: `vMAJOR.MINOR.PATCH`

- **MAJOR** (v2.0.0): Breaking changes, major redesign
- **MINOR** (v1.1.0): New features, backward-compatible
- **PATCH** (v1.0.5): Bug fixes, small improvements

Examples:
- `v1.0.4` → `v1.0.5`: Fixed bugs
- `v1.0.5` → `v1.1.0`: Added new feature
- `v1.5.0` → `v2.0.0`: Major rewrite

## Troubleshooting

### "Not a git repository" Error
- Make sure you're running from the `bible-search-lite` directory
- Check that `.git` folder exists

### "Failed to push" Error
- Make sure you have internet connection
- Check that you've configured git credentials
- Try: `git config --global user.name "Your Name"`
- Try: `git config --global user.email "your@email.com"`

### "Failed to create commit" Error
- Make sure you clicked "Stage All Changes" first
- Make sure you entered a commit message
- Check that files were actually changed

### "Tag already exists" Error
- You've already created this version tag
- Use a different version number (e.g., v1.0.6 instead of v1.0.5)

## Git Configuration (First Time)

If this is your first time using git, configure it:

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

For GitHub authentication, you may need a Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (full control)
4. Copy token
5. Use as password when git asks

## Safety Features

- Tool always shows what will be committed before committing
- Push requires confirmation
- Release creation shows next steps
- Can't accidentally delete history
- All operations use standard git commands

## What This Tool Does NOT Do

- Does NOT upload release files (database, installers)
  → You do this manually on GitHub.com
- Does NOT manage multiple branches
  → Assumes you work on `main` branch
- Does NOT resolve merge conflicts
  → Use git command line if conflicts occur

## Tips

1. **Commit Often:** Small commits are better than large ones
2. **Good Messages:** Explain WHY you changed something, not just WHAT
3. **Test Before Release:** Make sure everything works before creating a release
4. **Update VERSION.txt:** Tool does this automatically
5. **Keep Release Notes:** Users appreciate detailed notes

## Example Development Session

```
9:00 AM - Fix highlighting bug
  → Edit widgets.py
  → Commit: "Fix mouse event handling for highlighted verses"
  → Push to GitHub

10:30 AM - Add new feature
  → Edit bible_search_lite.py
  → Commit: "Add support for regex searches"
  → Push to GitHub

2:00 PM - Ready for release
  → Test everything
  → Create release v1.0.5
  → Upload database to GitHub release
  → Announce to users
```

## Support

For questions about:
- **This tool:** Check this guide
- **Git concepts:** https://git-scm.com/doc
- **GitHub releases:** https://docs.github.com/en/repositories/releasing-projects-on-github
- **Bible Search Lite:** See main README.md

---

**Remember:** This tool simplifies git/GitHub but doesn't replace understanding the basics. Take time to learn git concepts - it will make development much easier!
