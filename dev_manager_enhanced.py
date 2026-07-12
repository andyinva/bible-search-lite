#!/usr/bin/env python3
"""
Bible Search Lite - Enhanced Development Manager Tool

A comprehensive GUI tool for managing GitHub operations and releases.
NOT included in Bible Search Lite distribution - for developers only.

NEW FEATURES IN ENHANCED VERSION:
  • Automatic version incrementing (major, minor, patch)
  • GitHub API integration for creating releases directly
  • File upload to releases (bible_data.sql.gz, etc.)
  • Branch management (create, switch, merge)
  • Pull latest changes from GitHub
  • View diff of uncommitted changes
  • Automated changelog generation from commits
  • Release asset management

Author: Andrew Hopkins
Enhanced with additional automation features
"""

import sys
import subprocess
import os
import re
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QListWidget, QLineEdit, QMessageBox, QTabWidget,
                             QSplitter, QGroupBox, QRadioButton, QButtonGroup,
                             QComboBox, QFileDialog, QCheckBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


class VersionManager:
    """Helper class for managing semantic versioning"""
    
    def __init__(self, version_file='VERSION.txt'):
        """
        Initialize version manager
        
        Args:
            version_file: Path to the VERSION.txt file
        """
        self.version_file = version_file
    
    def get_current_version(self):
        """
        Read current version from VERSION.txt
        
        Returns:
            Current version string (e.g., 'v1.0.5') or 'v0.0.0' if not found
        """
        if os.path.exists(self.version_file):
            try:
                with open(self.version_file, 'r') as f:
                    return f.read().strip()
            except Exception:
                pass
        return 'v0.0.0'
    
    def parse_version(self, version_str):
        """
        Parse version string into components
        
        Args:
            version_str: Version string like 'v1.0.5'
            
        Returns:
            Tuple of (major, minor, patch) as integers
        """
        # Remove 'v' prefix if present
        clean_version = version_str.lstrip('v')
        
        # Parse major.minor.patch
        match = re.match(r'(\d+)\.(\d+)\.(\d+)', clean_version)
        if match:
            return tuple(map(int, match.groups()))
        return (0, 0, 0)
    
    def increment_version(self, bump_type='patch'):
        """
        Increment version based on bump type
        
        Args:
            bump_type: 'major', 'minor', or 'patch'
            
        Returns:
            New version string (e.g., 'v1.0.6')
        """
        current = self.get_current_version()
        major, minor, patch = self.parse_version(current)
        
        # Increment based on type
        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        return f'v{major}.{minor}.{patch}'
    
    def save_version(self, version):
        """
        Save version to VERSION.txt file
        
        Args:
            version: Version string to save (e.g., 'v1.0.6')
        """
        with open(self.version_file, 'w') as f:
            f.write(version + '\n')


class GitHubReleaseThread(QThread):
    """Background thread for creating GitHub releases via API"""
    
    # Signals for thread communication
    progress = pyqtSignal(str)  # Progress messages
    finished = pyqtSignal(bool, str)  # Success status and message
    
    def __init__(self, version, notes, is_prerelease, files_to_upload):
        """
        Initialize GitHub release thread
        
        Args:
            version: Version tag (e.g., 'v1.0.5')
            notes: Release notes text
            is_prerelease: Whether this is a pre-release
            files_to_upload: List of file paths to upload as assets
        """
        super().__init__()
        self.version = version
        self.notes = notes
        self.is_prerelease = is_prerelease
        self.files_to_upload = files_to_upload
    
    def run(self):
        """Execute the GitHub release creation process"""
        try:
            # Note: This requires GitHub CLI (gh) to be installed and authenticated
            # Check if gh is available
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.finished.emit(False, 
                    "GitHub CLI (gh) not found.\n\n" +
                    "Please install from: https://cli.github.com/\n" +
                    "Then run: gh auth login")
                return
            
            self.progress.emit("Creating git tag...")
            
            # Create git tag
            subprocess.run(['git', 'tag', '-a', self.version, '-m', self.notes], 
                         check=True)
            
            self.progress.emit("Pushing tag to GitHub...")
            
            # Push tag
            subprocess.run(['git', 'push', 'origin', self.version], check=True)
            
            self.progress.emit("Creating GitHub release...")
            
            # Create release using GitHub CLI
            gh_cmd = [
                'gh', 'release', 'create', self.version,
                '--notes', self.notes,
                '--title', self.version
            ]
            
            # Add prerelease flag if needed
            if self.is_prerelease:
                gh_cmd.append('--prerelease')
            
            # Add files to upload
            for file_path in self.files_to_upload:
                if os.path.exists(file_path):
                    gh_cmd.append(file_path)
                    self.progress.emit(f"Uploading {os.path.basename(file_path)}...")
            
            # Execute release creation
            result = subprocess.run(gh_cmd, capture_output=True, text=True, check=True)
            
            self.progress.emit("Release created successfully!")
            self.finished.emit(True, 
                f"Release {self.version} created successfully!\n\n" +
                f"Uploaded {len(self.files_to_upload)} file(s).\n\n" +
                f"View at: {result.stdout.strip()}")
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to create release:\n{e}\n\n"
            if e.stderr:
                error_msg += f"Error: {e.stderr}"
            self.finished.emit(False, error_msg)
        except Exception as e:
            self.finished.emit(False, f"Unexpected error: {e}")


class DevManagerWindow(QMainWindow):
    """Main window for enhanced development management tool"""

    def __init__(self):
        """Initialize the development manager window"""
        super().__init__()
        self.setWindowTitle("Bible Search Lite - Enhanced Development Manager")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize version manager
        self.version_mgr = VersionManager()
        
        # Track release thread
        self.release_thread = None

        # Check if we're in a git repository
        if not self.is_git_repo():
            QMessageBox.critical(self, "Error",
                                "Not a git repository!\n\n" +
                                "Please run this tool from the bible-search-lite directory.")
            sys.exit(1)

        self.setup_ui()
        self.load_data()

    def is_git_repo(self):
        """
        Check if current directory is a git repository
        
        Returns:
            True if in a git repo, False otherwise
        """
        try:
            subprocess.run(['git', 'status'], capture_output=True, check=True)
            return True
        except:
            return False

    def setup_ui(self):
        """Create the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Enhanced Development Manager")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Tab 1: Commit Management
        self.commit_tab = self.create_commit_tab()
        tabs.addTab(self.commit_tab, "📝 Commits")

        # Tab 2: Release Management (Enhanced)
        self.release_tab = self.create_release_tab()
        tabs.addTab(self.release_tab, "🚀 Releases")

        # Tab 3: Branch Management (NEW)
        self.branch_tab = self.create_branch_tab()
        tabs.addTab(self.branch_tab, "🌿 Branches")

        # Tab 4: History View
        self.history_tab = self.create_history_tab()
        tabs.addTab(self.history_tab, "📊 History")

        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def create_commit_tab(self):
        """
        Create the commit management tab with enhanced features
        
        Returns:
            QWidget containing the commit tab UI
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Current branch info
        branch_group = QGroupBox("Current Branch")
        branch_layout = QVBoxLayout(branch_group)
        self.branch_label = QLabel("Loading...")
        branch_layout.addWidget(self.branch_label)
        
        # Add pull button
        pull_btn = QPushButton("⬇️ Pull Latest Changes")
        pull_btn.clicked.connect(self.pull_from_github)
        branch_layout.addWidget(pull_btn)
        
        layout.addWidget(branch_group)

        # Git status with diff viewer
        status_group = QGroupBox("Uncommitted Changes")
        status_layout = QVBoxLayout(status_group)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        status_layout.addWidget(self.status_text)

        button_row = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Refresh Status")
        refresh_btn.clicked.connect(self.refresh_git_status)
        button_row.addWidget(refresh_btn)
        
        # NEW: View diff button
        diff_btn = QPushButton("📋 View Diff")
        diff_btn.clicked.connect(self.show_diff)
        button_row.addWidget(diff_btn)
        
        status_layout.addLayout(button_row)
        layout.addWidget(status_group)

        # Commit creation
        commit_group = QGroupBox("Create Commit")
        commit_layout = QVBoxLayout(commit_group)

        commit_layout.addWidget(QLabel("Commit Message:"))
        self.commit_message = QTextEdit()
        self.commit_message.setMaximumHeight(100)
        self.commit_message.setPlaceholderText(
            "Enter commit message here...\n\n" +
            "Example:\nFix search highlighting bug\n" +
            "- Fixed phrase matching\n- Improved performance"
        )
        commit_layout.addWidget(self.commit_message)

        button_layout = QHBoxLayout()

        stage_all_btn = QPushButton("📎 Stage All Changes")
        stage_all_btn.clicked.connect(self.stage_all_changes)
        button_layout.addWidget(stage_all_btn)

        commit_btn = QPushButton("✅ Commit")
        commit_btn.clicked.connect(self.create_commit)
        button_layout.addWidget(commit_btn)

        push_btn = QPushButton("⬆️ Push to GitHub")
        push_btn.clicked.connect(self.push_to_github)
        button_layout.addWidget(push_btn)

        commit_layout.addLayout(button_layout)
        layout.addWidget(commit_group)

        return widget

    def create_release_tab(self):
        """
        Create the enhanced release management tab
        
        Returns:
            QWidget containing the release tab UI
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Current version info
        version_group = QGroupBox("Current Version")
        version_layout = QVBoxLayout(version_group)
        self.version_label = QLabel("Loading...")
        version_layout.addWidget(self.version_label)
        layout.addWidget(version_group)

        # Create new release (ENHANCED)
        release_group = QGroupBox("Create New Release")
        release_layout = QVBoxLayout(release_group)

        # Version increment buttons (NEW)
        version_bump_layout = QHBoxLayout()
        version_bump_layout.addWidget(QLabel("Quick Version Bump:"))
        
        major_btn = QPushButton("Major (x.0.0)")
        major_btn.clicked.connect(lambda: self.bump_version('major'))
        version_bump_layout.addWidget(major_btn)
        
        minor_btn = QPushButton("Minor (0.x.0)")
        minor_btn.clicked.connect(lambda: self.bump_version('minor'))
        version_bump_layout.addWidget(minor_btn)
        
        patch_btn = QPushButton("Patch (0.0.x)")
        patch_btn.clicked.connect(lambda: self.bump_version('patch'))
        version_bump_layout.addWidget(patch_btn)
        
        release_layout.addLayout(version_bump_layout)

        # Manual version input
        version_input_layout = QHBoxLayout()
        version_input_layout.addWidget(QLabel("Or Enter Version:"))
        self.version_input = QLineEdit()
        self.version_input.setPlaceholderText("e.g., v1.0.5")
        version_input_layout.addWidget(self.version_input)
        release_layout.addLayout(version_input_layout)
        
        # NEW: Auto-generate changelog button
        changelog_layout = QHBoxLayout()
        changelog_btn = QPushButton("📝 Generate Changelog from Commits")
        changelog_btn.clicked.connect(self.generate_changelog)
        changelog_layout.addWidget(changelog_btn)
        release_layout.addLayout(changelog_layout)

        # Release notes
        release_layout.addWidget(QLabel("Release Notes:"))
        self.release_notes = QTextEdit()
        self.release_notes.setPlaceholderText(
            "Enter release notes here...\n\n" +
            "Example:\n" +
            "## What's New\n" +
            "- Fixed search term highlighting to preserve quoted phrases\n" +
            "- Improved comment functionality in Window 5\n\n" +
            "## Bug Fixes\n" +
            "- Fixed mouse event handling for highlighted verses"
        )
        release_layout.addWidget(self.release_notes)

        # Release type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Release Type:"))
        self.release_type_group = QButtonGroup()

        latest_radio = QRadioButton("Latest (recommended for users)")
        latest_radio.setChecked(True)
        self.release_type_group.addButton(latest_radio, 1)
        type_layout.addWidget(latest_radio)

        prerelease_radio = QRadioButton("Pre-release (beta/testing)")
        self.release_type_group.addButton(prerelease_radio, 2)
        type_layout.addWidget(prerelease_radio)

        release_layout.addLayout(type_layout)
        
        # NEW: File upload section
        files_group = QGroupBox("Release Files to Upload")
        files_layout = QVBoxLayout(files_group)
        
        self.release_files_list = QListWidget()
        self.release_files_list.setMaximumHeight(100)
        files_layout.addWidget(self.release_files_list)
        
        file_buttons = QHBoxLayout()
        add_file_btn = QPushButton("➕ Add File")
        add_file_btn.clicked.connect(self.add_release_file)
        file_buttons.addWidget(add_file_btn)
        
        remove_file_btn = QPushButton("➖ Remove Selected")
        remove_file_btn.clicked.connect(self.remove_release_file)
        file_buttons.addWidget(remove_file_btn)
        
        files_layout.addLayout(file_buttons)
        release_layout.addWidget(files_group)
        
        # Progress bar (NEW)
        self.release_progress = QProgressBar()
        self.release_progress.setVisible(False)
        release_layout.addWidget(self.release_progress)

        # Create release button (ENHANCED)
        create_release_btn = QPushButton("🚀 Create Release & Upload Files")
        create_release_btn.clicked.connect(self.create_release_with_files)
        release_layout.addWidget(create_release_btn)

        layout.addWidget(release_group)

        # Instructions (UPDATED)
        instructions = QLabel(
            "ℹ️ Enhanced Features:\n" +
            "• Auto-increment version numbers\n" +
            "• Generate changelog from git commits\n" +
            "• Upload files directly to release (requires GitHub CLI: gh)\n" +
            "• Creates full GitHub release automatically"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666; padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(instructions)

        return widget

    def create_branch_tab(self):
        """
        Create the branch management tab (NEW)
        
        Returns:
            QWidget containing the branch tab UI
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Current branches
        branch_group = QGroupBox("Branches")
        branch_layout = QVBoxLayout(branch_group)
        
        self.branch_list = QListWidget()
        branch_layout.addWidget(self.branch_list)
        
        branch_buttons = QHBoxLayout()
        
        refresh_branches_btn = QPushButton("🔄 Refresh")
        refresh_branches_btn.clicked.connect(self.load_branches)
        branch_buttons.addWidget(refresh_branches_btn)
        
        switch_branch_btn = QPushButton("🔀 Switch to Selected")
        switch_branch_btn.clicked.connect(self.switch_branch)
        branch_buttons.addWidget(switch_branch_btn)
        
        branch_layout.addLayout(branch_buttons)
        layout.addWidget(branch_group)
        
        # Create new branch
        new_branch_group = QGroupBox("Create New Branch")
        new_branch_layout = QVBoxLayout(new_branch_group)
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Branch Name:"))
        self.new_branch_name = QLineEdit()
        self.new_branch_name.setPlaceholderText("e.g., feature/new-search-option")
        name_layout.addWidget(self.new_branch_name)
        new_branch_layout.addLayout(name_layout)
        
        create_branch_btn = QPushButton("➕ Create Branch")
        create_branch_btn.clicked.connect(self.create_new_branch)
        new_branch_layout.addWidget(create_branch_btn)
        
        layout.addWidget(new_branch_group)
        
        # Merge branches
        merge_group = QGroupBox("Merge Branch")
        merge_layout = QVBoxLayout(merge_group)
        
        merge_layout.addWidget(QLabel("Merge selected branch into current branch:"))
        merge_btn = QPushButton("🔀 Merge Selected Branch")
        merge_btn.clicked.connect(self.merge_branch)
        merge_layout.addWidget(merge_btn)
        
        layout.addWidget(merge_group)
        
        layout.addStretch()
        
        return widget

    def create_history_tab(self):
        """
        Create the history view tab
        
        Returns:
            QWidget containing the history tab UI
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Split between dev commits and releases
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Development commits
        dev_group = QGroupBox("Recent Commits (Development)")
        dev_layout = QVBoxLayout(dev_group)
        self.dev_commits = QListWidget()
        dev_layout.addWidget(self.dev_commits)
        splitter.addWidget(dev_group)

        # Released versions
        release_group = QGroupBox("Released Versions")
        release_layout = QVBoxLayout(release_group)
        self.release_list = QListWidget()
        release_layout.addWidget(self.release_list)
        splitter.addWidget(release_group)

        layout.addWidget(splitter)

        return widget

    def load_data(self):
        """Load all data from git repository"""
        self.load_branch_info()
        self.load_version_info()
        self.load_commit_history()
        self.load_releases()
        self.load_branches()
        self.refresh_git_status()

    def refresh_git_status(self):
        """Refresh the git status display"""
        try:
            # Get git status in short format
            result = subprocess.run(['git', 'status', '--short'],
                                  capture_output=True, text=True, check=True)

            if result.stdout.strip():
                self.status_text.setPlainText(result.stdout)
                self.status_label.setText("Status: Uncommitted changes present")
            else:
                self.status_text.setPlainText("No uncommitted changes")
                self.status_label.setText("Status: Working directory clean")

        except Exception as e:
            self.status_text.setPlainText(f"Error: {e}")

    def load_branch_info(self):
        """Load current branch information"""
        try:
            result = subprocess.run(['git', 'branch', '--show-current'],
                                  capture_output=True, text=True, check=True)
            branch = result.stdout.strip()
            self.branch_label.setText(f"Branch: {branch}")
        except Exception as e:
            self.branch_label.setText(f"Error: {e}")

    def load_version_info(self):
        """Load current version from VERSION.txt and latest tag"""
        current_version = self.version_mgr.get_current_version()
        
        # Also get latest git tag
        try:
            result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                latest_tag = result.stdout.strip()
                version_text = f"{current_version} (Latest tag: {latest_tag})"
            else:
                version_text = current_version
        except:
            version_text = current_version

        self.version_label.setText(f"Current Version: {version_text}")

    def load_commit_history(self):
        """Load recent commits"""
        self.dev_commits.clear()
        try:
            # Get last 20 commits
            result = subprocess.run(['git', 'log', '--oneline', '--decorate', '-20'],
                                  capture_output=True, text=True, check=True)

            for line in result.stdout.strip().split('\n'):
                if line:
                    self.dev_commits.addItem(line)

        except Exception as e:
            self.dev_commits.addItem(f"Error: {e}")

    def load_releases(self):
        """Load all git tags (releases)"""
        self.release_list.clear()
        try:
            result = subprocess.run(['git', 'tag', '-l', '--sort=-version:refname'],
                                  capture_output=True, text=True, check=True)

            tags = result.stdout.strip().split('\n')
            for tag in tags:
                if tag:
                    # Get tag date
                    date_result = subprocess.run(
                        ['git', 'log', '-1', '--format=%ai', tag],
                        capture_output=True, text=True
                    )
                    date = date_result.stdout.strip().split()[0] if date_result.returncode == 0 else ""

                    self.release_list.addItem(f"{tag} - {date}")

        except Exception as e:
            self.release_list.addItem(f"Error: {e}")
    
    def load_branches(self):
        """Load all git branches (NEW)"""
        self.branch_list.clear()
        try:
            # Get all branches
            result = subprocess.run(['git', 'branch', '-a'],
                                  capture_output=True, text=True, check=True)
            
            current_branch_result = subprocess.run(['git', 'branch', '--show-current'],
                                                  capture_output=True, text=True, check=True)
            current_branch = current_branch_result.stdout.strip()
            
            for line in result.stdout.strip().split('\n'):
                branch = line.strip().lstrip('* ')
                if branch:
                    # Mark current branch
                    if branch == current_branch:
                        self.branch_list.addItem(f"* {branch} (current)")
                    else:
                        self.branch_list.addItem(branch)
        
        except Exception as e:
            self.branch_list.addItem(f"Error: {e}")

    def stage_all_changes(self):
        """Stage all changes for commit"""
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            self.status_label.setText("Status: All changes staged")
            self.refresh_git_status()
            QMessageBox.information(self, "Success", "All changes staged for commit")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stage changes:\n{e}")

    def create_commit(self):
        """Create a git commit"""
        message = self.commit_message.toPlainText().strip()

        if not message:
            QMessageBox.warning(self, "Warning", "Please enter a commit message")
            return

        try:
            # Add Claude Code attribution
            full_message = message + "\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"

            subprocess.run(['git', 'commit', '-m', full_message], check=True)

            self.status_label.setText("Status: Commit created successfully")
            self.commit_message.clear()
            self.refresh_git_status()
            self.load_commit_history()

            QMessageBox.information(self, "Success",
                                  "Commit created successfully!\n\n" +
                                  "Don't forget to push to GitHub.")

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error",
                               f"Failed to create commit:\n{e}\n\n" +
                               "Make sure you have staged changes.")

    def push_to_github(self):
        """Push commits to GitHub"""
        reply = QMessageBox.question(self, "Confirm Push",
                                    "Push all commits to GitHub?",
                                    QMessageBox.StandardButton.Yes |
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = subprocess.run(['git', 'push'],
                                      capture_output=True, text=True, check=True)

                self.status_label.setText("Status: Pushed to GitHub successfully")
                QMessageBox.information(self, "Success",
                                      "Commits pushed to GitHub!\n\n" + result.stdout)

            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error",
                                   f"Failed to push:\n{e.stderr}")
    
    def pull_from_github(self):
        """Pull latest changes from GitHub (NEW)"""
        reply = QMessageBox.question(self, "Confirm Pull",
                                    "Pull latest changes from GitHub?\n\n" +
                                    "Make sure you have committed local changes.",
                                    QMessageBox.StandardButton.Yes |
                                    QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                result = subprocess.run(['git', 'pull'],
                                      capture_output=True, text=True, check=True)
                
                self.status_label.setText("Status: Pulled from GitHub successfully")
                self.load_data()  # Refresh all data
                QMessageBox.information(self, "Success",
                                      "Pulled latest changes!\n\n" + result.stdout)
            
            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error",
                                   f"Failed to pull:\n{e.stderr}")
    
    def show_diff(self):
        """Show diff of uncommitted changes (NEW)"""
        try:
            result = subprocess.run(['git', 'diff'],
                                  capture_output=True, text=True, check=True)
            
            if not result.stdout.strip():
                QMessageBox.information(self, "No Changes",
                                      "No uncommitted changes to show.")
                return
            
            # Create dialog to show diff
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Git Diff")
            dialog.setText("Uncommitted Changes:")
            dialog.setDetailedText(result.stdout)
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            dialog.exec()
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to show diff:\n{e}")
    
    def bump_version(self, bump_type):
        """
        Auto-increment version number (NEW)
        
        Args:
            bump_type: 'major', 'minor', or 'patch'
        """
        new_version = self.version_mgr.increment_version(bump_type)
        self.version_input.setText(new_version)
        
        # Update display
        self.status_label.setText(f"Version bumped to {new_version}")
    
    def generate_changelog(self):
        """Generate changelog from recent commits (NEW)"""
        try:
            # Get commits since last tag
            result = subprocess.run(
                ['git', 'log', '--pretty=format:- %s', '--since="1 month ago"'],
                capture_output=True, text=True, check=True
            )
            
            if not result.stdout.strip():
                QMessageBox.information(self, "No Commits",
                                      "No recent commits to generate changelog from.")
                return
            
            # Format changelog
            changelog = "## What's New\n\n" + result.stdout
            
            # Append to release notes
            current_notes = self.release_notes.toPlainText()
            if current_notes:
                self.release_notes.setPlainText(current_notes + "\n\n" + changelog)
            else:
                self.release_notes.setPlainText(changelog)
            
            self.status_label.setText("Changelog generated from commits")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate changelog:\n{e}")
    
    def add_release_file(self):
        """Add file to release upload list (NEW)"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Upload",
            "",
            "All Files (*.*)"
        )
        
        if file_path:
            self.release_files_list.addItem(file_path)
    
    def remove_release_file(self):
        """Remove selected file from release upload list (NEW)"""
        current_item = self.release_files_list.currentItem()
        if current_item:
            self.release_files_list.takeItem(self.release_files_list.row(current_item))
    
    def create_release_with_files(self):
        """Create release and upload files using GitHub API (ENHANCED)"""
        version = self.version_input.text().strip()
        notes = self.release_notes.toPlainText().strip()

        if not version:
            QMessageBox.warning(self, "Warning", "Please enter a version tag (e.g., v1.0.5)")
            return

        if not notes:
            QMessageBox.warning(self, "Warning", "Please enter release notes")
            return

        # Validate version format
        if not version.startswith('v'):
            reply = QMessageBox.question(self, "Version Format",
                                        f"Version tag '{version}' doesn't start with 'v'.\n" +
                                        f"Use 'v{version}' instead?",
                                        QMessageBox.StandardButton.Yes |
                                        QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                version = f"v{version}"
            else:
                return

        is_prerelease = self.release_type_group.checkedId() == 2
        
        # Get files to upload
        files_to_upload = []
        for i in range(self.release_files_list.count()):
            files_to_upload.append(self.release_files_list.item(i).text())
        
        # Confirm with user
        file_list = "\n".join([os.path.basename(f) for f in files_to_upload])
        confirm_msg = f"Create release {version}?\n\n"
        confirm_msg += f"Type: {'Pre-release' if is_prerelease else 'Latest'}\n\n"
        if files_to_upload:
            confirm_msg += f"Files to upload:\n{file_list}"
        else:
            confirm_msg += "No files to upload"
        
        reply = QMessageBox.question(self, "Confirm Release",
                                    confirm_msg,
                                    QMessageBox.StandardButton.Yes |
                                    QMessageBox.StandardButton.No)
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Create and start release thread
        self.release_thread = GitHubReleaseThread(
            version, notes, is_prerelease, files_to_upload
        )
        
        # Connect signals
        self.release_thread.progress.connect(self.on_release_progress)
        self.release_thread.finished.connect(self.on_release_finished)
        
        # Show progress bar
        self.release_progress.setVisible(True)
        self.release_progress.setRange(0, 0)  # Indeterminate
        
        # Start thread
        self.release_thread.start()
    
    def on_release_progress(self, message):
        """
        Handle progress updates from release thread
        
        Args:
            message: Progress message to display
        """
        self.status_label.setText(f"Status: {message}")
    
    def on_release_finished(self, success, message):
        """
        Handle completion of release creation
        
        Args:
            success: Whether the release was successful
            message: Result message
        """
        # Hide progress bar
        self.release_progress.setVisible(False)
        
        if success:
            # Save version to VERSION.txt
            version = self.version_input.text().strip()
            self.version_mgr.save_version(version)
            
            # Clear form
            self.version_input.clear()
            self.release_notes.clear()
            self.release_files_list.clear()
            
            # Reload data
            self.load_data()
            
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def create_new_branch(self):
        """Create a new git branch (NEW)"""
        branch_name = self.new_branch_name.text().strip()
        
        if not branch_name:
            QMessageBox.warning(self, "Warning", "Please enter a branch name")
            return
        
        try:
            # Create and switch to new branch
            subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
            
            self.status_label.setText(f"Created and switched to branch: {branch_name}")
            self.new_branch_name.clear()
            self.load_branches()
            self.load_branch_info()
            
            QMessageBox.information(self, "Success",
                                  f"Created new branch: {branch_name}")
        
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to create branch:\n{e}")
    
    def switch_branch(self):
        """Switch to selected branch (NEW)"""
        current_item = self.branch_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a branch")
            return
        
        # Extract branch name (remove markers)
        branch_text = current_item.text()
        branch_name = branch_text.replace('* ', '').replace(' (current)', '').strip()
        
        # Don't switch if already on this branch
        if '(current)' in branch_text:
            QMessageBox.information(self, "Already There",
                                  f"Already on branch: {branch_name}")
            return
        
        try:
            subprocess.run(['git', 'checkout', branch_name], check=True)
            
            self.status_label.setText(f"Switched to branch: {branch_name}")
            self.load_branches()
            self.load_branch_info()
            
            QMessageBox.information(self, "Success",
                                  f"Switched to branch: {branch_name}")
        
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to switch branch:\n{e}")
    
    def merge_branch(self):
        """Merge selected branch into current branch (NEW)"""
        current_item = self.branch_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a branch to merge")
            return
        
        # Extract branch name
        branch_text = current_item.text()
        if '(current)' in branch_text:
            QMessageBox.warning(self, "Cannot Merge",
                              "Cannot merge a branch into itself")
            return
        
        branch_name = branch_text.replace('* ', '').strip()
        
        # Confirm merge
        reply = QMessageBox.question(self, "Confirm Merge",
                                    f"Merge {branch_name} into current branch?",
                                    QMessageBox.StandardButton.Yes |
                                    QMessageBox.StandardButton.No)
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        try:
            result = subprocess.run(['git', 'merge', branch_name],
                                  capture_output=True, text=True, check=True)
            
            self.status_label.setText(f"Merged {branch_name}")
            self.load_data()
            
            QMessageBox.information(self, "Success",
                                  f"Merged {branch_name}!\n\n" + result.stdout)
        
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error",
                               f"Failed to merge:\n{e.stderr}\n\n" +
                               "You may need to resolve conflicts manually.")


def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    window = DevManagerWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
