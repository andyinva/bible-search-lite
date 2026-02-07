#!/usr/bin/env python3
"""
Bible Search Lite - Release Wizard

A comprehensive step-by-step GUI tool that guides you through the entire
release process from version updates to GitHub release publication.

Features:
  • Sequential step-by-step workflow
  • Automated file updates (VERSION.txt, setup.py, setup_win11.py)
  • Database export automation
  • Git commit, tag, and push operations
  • GitHub release creation with file uploads
  • Built-in authentication checking
  • Progress tracking with visual indicators
  • Detailed instructions for each step

Author: Andrew Hopkins
"""

import sys
import subprocess
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QLineEdit, QMessageBox,
    QScrollArea, QFrame, QProgressBar, QListWidget, QFileDialog,
    QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette


# ============================================================================
# STEP CONFIGURATION
# ============================================================================

STEPS = [
    {
        "number": 1,
        "title": "Version Number",
        "short_title": "Version",
        "description": "Set the version number for this release"
    },
    {
        "number": 2,
        "title": "Release Notes",
        "short_title": "Notes",
        "description": "Create release notes and changelog"
    },
    {
        "number": 3,
        "title": "Update Files",
        "short_title": "Update Files",
        "description": "Update version in all project files"
    },
    {
        "number": 4,
        "title": "Export Database",
        "short_title": "Export DB",
        "description": "Export and compress the Bible database"
    },
    {
        "number": 5,
        "title": "Git Status",
        "short_title": "Git Status",
        "description": "Review changes and stage files"
    },
    {
        "number": 6,
        "title": "Git Commit",
        "short_title": "Commit",
        "description": "Create a git commit"
    },
    {
        "number": 7,
        "title": "Git Tag",
        "short_title": "Tag",
        "description": "Create a version tag"
    },
    {
        "number": 8,
        "title": "Git Push",
        "short_title": "Push",
        "description": "Push commits and tags to GitHub"
    },
    {
        "number": 9,
        "title": "GitHub Release",
        "short_title": "Release",
        "description": "Create GitHub release and upload files"
    },
    {
        "number": 10,
        "title": "Complete",
        "short_title": "Done",
        "description": "Release published successfully!"
    }
]


# ============================================================================
# VERSION MANAGER
# ============================================================================

class VersionManager:
    """Helper class for managing semantic versioning"""
    
    def __init__(self, version_file='VERSION.txt'):
        """Initialize version manager"""
        self.version_file = version_file
    
    def get_current_version(self):
        """Read current version from VERSION.txt"""
        if os.path.exists(self.version_file):
            try:
                with open(self.version_file, 'r') as f:
                    return f.read().strip()
            except Exception:
                pass
        return 'v0.0.0'
    
    def parse_version(self, version_str):
        """Parse version string into components"""
        clean_version = version_str.lstrip('v')
        match = re.match(r'(\d+)\.(\d+)\.(\d+)', clean_version)
        if match:
            return tuple(map(int, match.groups()))
        return (0, 0, 0)
    
    def increment_version(self, bump_type='patch'):
        """Increment version based on bump type"""
        current = self.get_current_version()
        major, minor, patch = self.parse_version(current)
        
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
        """Save version to VERSION.txt file"""
        with open(self.version_file, 'w') as f:
            f.write(version + '\n')


# ============================================================================
# FILE UPDATER
# ============================================================================

class FileUpdater:
    """Helper class for updating version numbers in project files"""
    
    @staticmethod
    def update_setup_py(version):
        """Update RELEASE_VERSION in setup.py"""
        if not os.path.exists('setup.py'):
            return False, "setup.py not found"
        
        try:
            with open('setup.py', 'r') as f:
                content = f.read()
            
            # Find and replace the RELEASE_VERSION line
            pattern = r'RELEASE_VERSION = "v[\d.]+"'
            replacement = f'RELEASE_VERSION = "{version}"'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content == content:
                return False, "RELEASE_VERSION line not found in setup.py"
            
            with open('setup.py', 'w') as f:
                f.write(new_content)
            
            return True, "Updated setup.py"
        
        except Exception as e:
            return False, f"Error updating setup.py: {e}"
    
    @staticmethod
    def update_setup_win11_py(version):
        """Update RELEASE_VERSION in setup_win11.py"""
        if not os.path.exists('setup_win11.py'):
            return False, "setup_win11.py not found"
        
        try:
            with open('setup_win11.py', 'r') as f:
                content = f.read()
            
            # Find and replace the RELEASE_VERSION line
            pattern = r'RELEASE_VERSION = "v[\d.]+"'
            replacement = f'RELEASE_VERSION = "{version}"'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content == content:
                return False, "RELEASE_VERSION line not found in setup_win11.py"
            
            with open('setup_win11.py', 'w') as f:
                f.write(new_content)
            
            return True, "Updated setup_win11.py"
        
        except Exception as e:
            return False, f"Error updating setup_win11.py: {e}"

    @staticmethod
    def update_bible_search_lite_py(version):
        """Update VERSION and date in bible_search_lite.py"""
        if not os.path.exists('bible_search_lite.py'):
            return False, "bible_search_lite.py not found"

        try:
            with open('bible_search_lite.py', 'r') as f:
                content = f.read()

            # Strip 'v' prefix from version for the VERSION variable
            version_num = version.lstrip('v')

            # Find and replace the VERSION line (e.g., VERSION = "1.1.3")
            version_pattern = r'VERSION = "[\d.]+"'
            version_replacement = f'VERSION = "{version_num}"'

            new_content = re.sub(version_pattern, version_replacement, content)

            if new_content == content:
                return False, "VERSION line not found in bible_search_lite.py"

            # Update the date in the window title
            # Get current month and year (e.g., "February 2026")
            from datetime import datetime
            current_date = datetime.now().strftime("%B %Y")

            # Find and replace the setWindowTitle line with the date
            title_pattern = r'self\.setWindowTitle\(f"Bible Search Lite v\{VERSION\} \([^)]+\)"\)'
            title_replacement = f'self.setWindowTitle(f"Bible Search Lite v{{VERSION}} ({current_date})")'

            new_content = re.sub(title_pattern, title_replacement, new_content)

            with open('bible_search_lite.py', 'w') as f:
                f.write(new_content)

            return True, f"Updated bible_search_lite.py (VERSION = {version_num}, date = {current_date})"

        except Exception as e:
            return False, f"Error updating bible_search_lite.py: {e}"


# ============================================================================
# BACKGROUND WORKER THREADS
# ============================================================================

class ExportDatabaseThread(QThread):
    """Background thread for exporting database"""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def run(self):
        """Execute the database export"""
        try:
            self.progress.emit("Running export_bible_data.py...")
            
            # Check if export script exists
            if not os.path.exists('export_bible_data.py'):
                self.finished.emit(False, "export_bible_data.py not found in current directory")
                return
            
            # Run the export script
            result = subprocess.run(
                [sys.executable, 'export_bible_data.py'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Check if files were created
                if os.path.exists('data/bible_data.sql.gz') and os.path.exists('data/checksums.txt'):
                    gz_size = os.path.getsize('data/bible_data.sql.gz') / (1024 * 1024)
                    self.finished.emit(True, 
                        f"Export successful!\n\n" +
                        f"Created files:\n" +
                        f"  • bible_data.sql.gz ({gz_size:.1f} MB)\n" +
                        f"  • checksums.txt\n\n" +
                        f"Files are ready for GitHub Release upload.")
                else:
                    self.finished.emit(False, "Export script ran but files were not created")
            else:
                self.finished.emit(False, 
                    f"Export failed:\n{result.stderr}")
        
        except Exception as e:
            self.finished.emit(False, f"Error running export: {e}")


class GitHubReleaseThread(QThread):
    """Background thread for creating GitHub releases"""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str, str)  # success, message, release_url
    
    def __init__(self, version, notes, is_prerelease, files_to_upload):
        super().__init__()
        self.version = version
        self.notes = notes
        self.is_prerelease = is_prerelease
        self.files_to_upload = files_to_upload
    
    def run(self):
        """Execute the GitHub release creation"""
        try:
            # Check if gh is available
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.finished.emit(False, 
                    "GitHub CLI (gh) not found.\n\n" +
                    "Please install from: https://cli.github.com/\n" +
                    "Then run: gh auth login", "")
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
                '--title', f'Bible Search Lite {self.version}'
            ]
            
            if self.is_prerelease:
                gh_cmd.append('--prerelease')
            
            # Add files to upload
            for file_path in self.files_to_upload:
                if os.path.exists(file_path):
                    gh_cmd.append(file_path)
                    self.progress.emit(f"Uploading {os.path.basename(file_path)}...")
            
            # Execute release creation
            result = subprocess.run(gh_cmd, capture_output=True, text=True, check=True)
            
            # Extract URL from output
            release_url = result.stdout.strip()
            
            self.progress.emit("Release created successfully!")
            self.finished.emit(True, 
                f"Release {self.version} created successfully!\n\n" +
                f"Uploaded {len(self.files_to_upload)} file(s).",
                release_url)
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to create release:\n{e}\n\n"
            if e.stderr:
                error_msg += f"Error: {e.stderr}"
            self.finished.emit(False, error_msg, "")
        except Exception as e:
            self.finished.emit(False, f"Unexpected error: {e}", "")


# ============================================================================
# STEP WIDGET BASE CLASS
# ============================================================================

class StepWidget(QWidget):
    """Base class for step widgets"""
    
    step_completed = pyqtSignal()
    
    def __init__(self, step_info, parent=None):
        super().__init__(parent)
        self.step_info = step_info
        self.is_completed = False
        self.setup_ui()
    
    def setup_ui(self):
        """Override this in subclasses"""
        pass
    
    def mark_completed(self):
        """Mark this step as completed"""
        self.is_completed = True
        self.step_completed.emit()
    
    def get_data(self):
        """Override to return step data"""
        return {}


# ============================================================================
# INDIVIDUAL STEP WIDGETS
# ============================================================================

class Step1VersionWidget(StepWidget):
    """Step 1: Set version number"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "<h3>Set Release Version</h3>"
            "<p>Choose the version number for this release. You can use the "
            "increment buttons for semantic versioning or enter a custom version.</p>"
            "<p><b>Semantic Versioning Guidelines:</b></p>"
            "<ul>"
            "<li><b>Major (x.0.0):</b> Breaking changes or major new features</li>"
            "<li><b>Minor (0.x.0):</b> New features, backward compatible</li>"
            "<li><b>Patch (0.0.x):</b> Bug fixes and small improvements</li>"
            "</ul>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Version manager
        self.version_mgr = VersionManager()
        
        # Current version display
        current_version = self.version_mgr.get_current_version()
        current_label = QLabel(f"<b>Current Version:</b> {current_version}")
        current_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(current_label)
        
        # Quick increment buttons
        bump_layout = QHBoxLayout()
        
        major_btn = QPushButton("Major (x.0.0)")
        major_btn.clicked.connect(lambda: self.bump_version('major'))
        bump_layout.addWidget(major_btn)
        
        minor_btn = QPushButton("Minor (0.x.0)")
        minor_btn.clicked.connect(lambda: self.bump_version('minor'))
        bump_layout.addWidget(minor_btn)
        
        patch_btn = QPushButton("Patch (0.0.x)")
        patch_btn.clicked.connect(lambda: self.bump_version('patch'))
        bump_layout.addWidget(patch_btn)
        
        layout.addLayout(bump_layout)
        
        # Manual version input
        manual_layout = QHBoxLayout()
        manual_layout.addWidget(QLabel("Or enter manually:"))
        self.version_input = QLineEdit()
        self.version_input.setPlaceholderText("e.g., v1.2.0")
        manual_layout.addWidget(self.version_input)
        layout.addLayout(manual_layout)
        
        # Next button
        layout.addStretch()
        self.next_btn = QPushButton("✓ Set Version and Continue")
        self.next_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.next_btn.clicked.connect(self.validate_and_continue)
        layout.addWidget(self.next_btn)
    
    def bump_version(self, bump_type):
        """Auto-increment version"""
        new_version = self.version_mgr.increment_version(bump_type)
        self.version_input.setText(new_version)
    
    def validate_and_continue(self):
        """Validate version and proceed"""
        version = self.version_input.text().strip()
        
        if not version:
            QMessageBox.warning(self, "Version Required", 
                              "Please enter a version number or use one of the increment buttons.")
            return
        
        # Ensure version starts with 'v'
        if not version.startswith('v'):
            version = 'v' + version
            self.version_input.setText(version)
        
        # Validate format
        if not re.match(r'v\d+\.\d+\.\d+', version):
            QMessageBox.warning(self, "Invalid Format",
                              "Version must be in format: v1.2.3")
            return
        
        # Confirm
        reply = QMessageBox.question(self, "Confirm Version",
                                    f"Set release version to {version}?",
                                    QMessageBox.StandardButton.Yes |
                                    QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.mark_completed()
    
    def get_data(self):
        return {"version": self.version_input.text().strip()}


class Step2NotesWidget(StepWidget):
    """Step 2: Create release notes"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "<h3>Create Release Notes</h3>"
            "<p>Write or generate release notes for this version. "
            "These will be used in your GitHub release.</p>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Generate changelog button
        gen_btn = QPushButton("📝 Generate Changelog from Git Commits")
        gen_btn.clicked.connect(self.generate_changelog)
        layout.addWidget(gen_btn)
        
        # Release notes text area
        layout.addWidget(QLabel("<b>Release Notes:</b>"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText(
            "Enter release notes here...\n\n"
            "Example:\n\n"
            "## What's New\n"
            "- Added two-color highlighting feature\n"
            "- Improved search performance\n\n"
            "## Bug Fixes\n"
            "- Fixed apostrophe handling\n"
            "- Corrected wildcard matching"
        )
        layout.addWidget(self.notes_edit)
        
        # Next button
        self.next_btn = QPushButton("✓ Save Notes and Continue")
        self.next_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.next_btn.clicked.connect(self.save_and_continue)
        layout.addWidget(self.next_btn)
    
    def generate_changelog(self):
        """Generate changelog from git commits"""
        try:
            result = subprocess.run(
                ['git', 'log', '--pretty=format:- %s', '--since="1 month ago"'],
                capture_output=True, text=True, check=True
            )
            
            if result.stdout.strip():
                changelog = "## Recent Changes\n\n" + result.stdout
                current_notes = self.notes_edit.toPlainText()
                if current_notes:
                    self.notes_edit.setPlainText(current_notes + "\n\n" + changelog)
                else:
                    self.notes_edit.setPlainText(changelog)
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not generate changelog: {e}")
    
    def save_and_continue(self):
        """Save release notes and proceed"""
        notes = self.notes_edit.toPlainText().strip()
        
        if not notes:
            reply = QMessageBox.question(self, "Empty Notes",
                                        "Release notes are empty. Continue anyway?",
                                        QMessageBox.StandardButton.Yes |
                                        QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        self.mark_completed()
    
    def get_data(self):
        return {"notes": self.notes_edit.toPlainText().strip()}


class Step3UpdateFilesWidget(StepWidget):
    """Step 3: Update version in project files"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "<h3>Update Project Files</h3>"
            "<p>This step will update the version number in all necessary project files:</p>"
            "<ul>"
            "<li>VERSION.txt</li>"
            "<li>setup.py (RELEASE_VERSION line)</li>"
            "<li>setup_win11.py (RELEASE_VERSION line)</li>"
            "<li>bible_search_lite.py (VERSION variable and window title date)</li>"
            "</ul>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Status display
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        layout.addWidget(self.status_text)
        
        # Update button
        layout.addStretch()
        self.update_btn = QPushButton("🔄 Update All Files")
        self.update_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold;")
        self.update_btn.clicked.connect(self.update_files)
        layout.addWidget(self.update_btn)
        
        # Next button (initially disabled)
        self.next_btn = QPushButton("✓ Continue")
        self.next_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.mark_completed)
        layout.addWidget(self.next_btn)
    
    def update_files(self):
        """Update version in all project files"""
        # Get version from parent wizard
        wizard = self.get_wizard()
        if not wizard:
            return
        
        version = wizard.get_step_data(1).get('version', '')
        if not version:
            QMessageBox.warning(self, "No Version", "Version not set in Step 1")
            return
        
        self.status_text.clear()
        self.status_text.append(f"Updating files to version {version}...\n")
        
        all_success = True
        
        # Update VERSION.txt
        version_mgr = VersionManager()
        try:
            version_mgr.save_version(version)
            self.status_text.append("✅ Updated VERSION.txt")
        except Exception as e:
            self.status_text.append(f"❌ Failed to update VERSION.txt: {e}")
            all_success = False
        
        # Update setup.py
        success, msg = FileUpdater.update_setup_py(version)
        if success:
            self.status_text.append(f"✅ {msg}")
        else:
            self.status_text.append(f"❌ {msg}")
            all_success = False
        
        # Update setup_win11.py
        success, msg = FileUpdater.update_setup_win11_py(version)
        if success:
            self.status_text.append(f"✅ {msg}")
        else:
            self.status_text.append(f"⚠️  {msg}")

        # Update bible_search_lite.py (VERSION and date in window title)
        success, msg = FileUpdater.update_bible_search_lite_py(version)
        if success:
            self.status_text.append(f"✅ {msg}")
        else:
            self.status_text.append(f"❌ {msg}")
            all_success = False

        if all_success:
            self.status_text.append("\n✅ All files updated successfully!")
            self.next_btn.setEnabled(True)
        else:
            self.status_text.append("\n⚠️  Some updates failed. Check messages above.")
    
    def get_wizard(self):
        """Get reference to parent wizard"""
        parent = self.parent()
        while parent:
            if isinstance(parent, ReleaseWizard):
                return parent
            parent = parent.parent()
        return None
    
    def get_data(self):
        return {"files_updated": self.next_btn.isEnabled()}


class Step4ExportDBWidget(StepWidget):
    """Step 4: Export database"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "<h3>Export Bible Database</h3>"
            "<p>This step runs <code>export_bible_data.py</code> to create distribution files:</p>"
            "<ul>"
            "<li>data/bible_data.sql.gz (compressed database)</li>"
            "<li>data/checksums.txt (SHA256 verification)</li>"
            "</ul>"
            "<p>These files will be uploaded to the GitHub release.</p>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Status display
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Export button
        layout.addStretch()
        self.export_btn = QPushButton("📦 Export Database")
        self.export_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold;")
        self.export_btn.clicked.connect(self.export_database)
        layout.addWidget(self.export_btn)
        
        # Next button (initially disabled)
        self.next_btn = QPushButton("✓ Continue")
        self.next_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.mark_completed)
        layout.addWidget(self.next_btn)
        
        self.export_thread = None
    
    def export_database(self):
        """Run database export"""
        self.status_text.clear()
        self.status_text.append("Starting database export...\n")
        self.export_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        
        # Create and start export thread
        self.export_thread = ExportDatabaseThread()
        self.export_thread.progress.connect(self.on_progress)
        self.export_thread.finished.connect(self.on_finished)
        self.export_thread.start()
    
    def on_progress(self, message):
        """Handle progress updates"""
        self.status_text.append(message)
    
    def on_finished(self, success, message):
        """Handle export completion"""
        self.progress_bar.setVisible(False)
        self.export_btn.setEnabled(True)
        
        if success:
            self.status_text.append(f"\n✅ {message}")
            self.next_btn.setEnabled(True)
        else:
            self.status_text.append(f"\n❌ {message}")
            QMessageBox.critical(self, "Export Failed", message)
    
    def get_data(self):
        return {"export_completed": self.next_btn.isEnabled()}


class Step5GitStatusWidget(StepWidget):
    """Step 5: Check git status and stage files"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "<h3>Review Git Changes</h3>"
            "<p>Review the changes that will be committed. "
            "Click 'Stage All Files' to prepare them for commit.</p>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Git status display
        layout.addWidget(QLabel("<b>Changed Files:</b>"))
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(200)
        layout.addWidget(self.status_text)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh Status")
        refresh_btn.clicked.connect(self.refresh_status)
        btn_layout.addWidget(refresh_btn)
        
        self.stage_btn = QPushButton("📎 Stage All Files")
        self.stage_btn.clicked.connect(self.stage_files)
        btn_layout.addWidget(self.stage_btn)
        
        layout.addLayout(btn_layout)
        
        # Next button (initially disabled)
        layout.addStretch()
        self.next_btn = QPushButton("✓ Continue")
        self.next_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.mark_completed)
        layout.addWidget(self.next_btn)
        
        # Auto-refresh on show
        QTimer.singleShot(100, self.refresh_status)
    
    def refresh_status(self):
        """Refresh git status"""
        try:
            result = subprocess.run(['git', 'status', '--short'],
                                  capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                self.status_text.setPlainText(result.stdout)
            else:
                self.status_text.setPlainText("No uncommitted changes")
                self.next_btn.setEnabled(True)
        
        except Exception as e:
            self.status_text.setPlainText(f"Error: {e}")
    
    def stage_files(self):
        """Stage all files for commit"""
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            QMessageBox.information(self, "Success", "All files staged for commit")
            self.refresh_status()
            self.next_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to stage files: {e}")
    
    def get_data(self):
        return {"files_staged": self.next_btn.isEnabled()}


class Step6GitCommitWidget(StepWidget):
    """Step 6: Create git commit"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "<h3>Create Git Commit</h3>"
            "<p>Write a commit message describing the changes in this release.</p>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Auto-generate commit message button
        gen_btn = QPushButton("📝 Generate Commit Message")
        gen_btn.clicked.connect(self.generate_commit_message)
        layout.addWidget(gen_btn)
        
        # Commit message editor
        layout.addWidget(QLabel("<b>Commit Message:</b>"))
        self.commit_edit = QTextEdit()
        self.commit_edit.setPlaceholderText(
            "Enter commit message...\n\n"
            "Example:\n"
            "Release v1.2.0: Enhanced search features\n\n"
            "- Added two-color highlighting\n"
            "- Improved wildcard matching\n"
            "- Updated database with 39 translations"
        )
        layout.addWidget(self.commit_edit)
        
        # Commit button
        layout.addStretch()
        self.commit_btn = QPushButton("✅ Create Commit")
        self.commit_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold;")
        self.commit_btn.clicked.connect(self.create_commit)
        layout.addWidget(self.commit_btn)
        
        # Next button (initially disabled)
        self.next_btn = QPushButton("✓ Continue")
        self.next_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.mark_completed)
        layout.addWidget(self.next_btn)
    
    def generate_commit_message(self):
        """Generate commit message from version and notes"""
        wizard = self.get_wizard()
        if not wizard:
            return
        
        version = wizard.get_step_data(1).get('version', '')
        notes = wizard.get_step_data(2).get('notes', '')
        
        if version:
            message = f"Release {version}"
            if notes:
                # Use first line of notes as summary
                first_line = notes.split('\n')[0].strip('#').strip()
                if first_line:
                    message = f"Release {version}: {first_line}"
                
                message += f"\n\n{notes}"
            
            self.commit_edit.setPlainText(message)
    
    def create_commit(self):
        """Create the git commit"""
        message = self.commit_edit.toPlainText().strip()
        
        if not message:
            QMessageBox.warning(self, "Empty Message", "Please enter a commit message")
            return
        
        try:
            subprocess.run(['git', 'commit', '-m', message], check=True)
            QMessageBox.information(self, "Success", "Commit created successfully!")
            self.next_btn.setEnabled(True)
            self.commit_btn.setEnabled(False)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", 
                               f"Failed to create commit: {e}\n\n"
                               "Make sure you have staged changes.")
    
    def get_wizard(self):
        """Get reference to parent wizard"""
        parent = self.parent()
        while parent:
            if isinstance(parent, ReleaseWizard):
                return parent
            parent = parent.parent()
        return None
    
    def get_data(self):
        return {"commit_created": self.next_btn.isEnabled(),
                "commit_message": self.commit_edit.toPlainText().strip()}


class Step7GitTagWidget(StepWidget):
    """Step 7: Create git tag"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "<h3>Create Git Tag</h3>"
            "<p>Create a version tag for this release. The tag will be used "
            "to identify this release in GitHub.</p>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Version display
        self.version_label = QLabel()
        self.version_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(self.version_label)
        
        # Status display
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        layout.addWidget(self.status_text)
        
        # Create tag button
        layout.addStretch()
        self.tag_btn = QPushButton("🏷️  Create Tag")
        self.tag_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold;")
        self.tag_btn.clicked.connect(self.create_tag)
        layout.addWidget(self.tag_btn)
        
        # Next button (initially disabled)
        self.next_btn = QPushButton("✓ Continue")
        self.next_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.mark_completed)
        layout.addWidget(self.next_btn)
        
        # Update version on show
        QTimer.singleShot(100, self.update_version_display)
    
    def update_version_display(self):
        """Update version display"""
        wizard = self.get_wizard()
        if wizard:
            version = wizard.get_step_data(1).get('version', '')
            self.version_label.setText(f"<b>Tag to create:</b> {version}")
    
    def create_tag(self):
        """Create git tag"""
        wizard = self.get_wizard()
        if not wizard:
            return
        
        version = wizard.get_step_data(1).get('version', '')
        notes = wizard.get_step_data(2).get('notes', 'Release ' + version)
        
        if not version:
            QMessageBox.warning(self, "No Version", "Version not set")
            return
        
        self.status_text.clear()
        
        try:
            # Check if tag exists
            result = subprocess.run(['git', 'tag', '-l', version],
                                  capture_output=True, text=True)
            
            if result.stdout.strip():
                reply = QMessageBox.question(self, "Tag Exists",
                                            f"Tag {version} already exists. Force update?",
                                            QMessageBox.StandardButton.Yes |
                                            QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    subprocess.run(['git', 'tag', '-d', version], check=True)
                    self.status_text.append(f"Deleted existing tag {version}")
                else:
                    return
            
            # Create tag
            subprocess.run(['git', 'tag', '-a', version, '-m', notes], check=True)
            self.status_text.append(f"✅ Created tag {version}")
            
            self.next_btn.setEnabled(True)
            self.tag_btn.setEnabled(False)
        
        except Exception as e:
            self.status_text.append(f"❌ Error: {e}")
            QMessageBox.critical(self, "Error", f"Failed to create tag: {e}")
    
    def get_wizard(self):
        """Get reference to parent wizard"""
        parent = self.parent()
        while parent:
            if isinstance(parent, ReleaseWizard):
                return parent
            parent = parent.parent()
        return None
    
    def get_data(self):
        return {"tag_created": self.next_btn.isEnabled()}


class Step8GitPushWidget(StepWidget):
    """Step 8: Push to GitHub"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "<h3>Push to GitHub</h3>"
            "<p>Push your commits and tags to GitHub. This makes them available "
            "for creating the release.</p>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Status display
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        # Push buttons
        layout.addStretch()
        btn_layout = QHBoxLayout()
        
        self.push_commits_btn = QPushButton("⬆️  Push Commits")
        self.push_commits_btn.clicked.connect(self.push_commits)
        btn_layout.addWidget(self.push_commits_btn)
        
        self.push_tags_btn = QPushButton("🏷️  Push Tags")
        self.push_tags_btn.clicked.connect(self.push_tags)
        btn_layout.addWidget(self.push_tags_btn)
        
        layout.addLayout(btn_layout)
        
        # Next button (initially disabled)
        self.next_btn = QPushButton("✓ Continue")
        self.next_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.mark_completed)
        layout.addWidget(self.next_btn)
        
        self.commits_pushed = False
        self.tags_pushed = False
    
    def push_commits(self):
        """Push commits to GitHub"""
        self.status_text.clear()
        self.status_text.append("Pushing commits to GitHub...\n")
        
        try:
            result = subprocess.run(['git', 'push'],
                                  capture_output=True, text=True, check=True)
            
            self.status_text.append("✅ Commits pushed successfully")
            if result.stdout:
                self.status_text.append(result.stdout)
            
            self.commits_pushed = True
            self.push_commits_btn.setEnabled(False)
            self.check_all_pushed()
        
        except subprocess.CalledProcessError as e:
            self.status_text.append(f"❌ Push failed: {e.stderr}")
            QMessageBox.critical(self, "Error", f"Failed to push commits:\n{e.stderr}")
    
    def push_tags(self):
        """Push tags to GitHub"""
        wizard = self.get_wizard()
        if not wizard:
            return
        
        version = wizard.get_step_data(1).get('version', '')
        if not version:
            return
        
        self.status_text.append(f"\nPushing tag {version} to GitHub...\n")
        
        try:
            result = subprocess.run(['git', 'push', 'origin', version],
                                  capture_output=True, text=True, check=True)
            
            self.status_text.append(f"✅ Tag {version} pushed successfully")
            if result.stdout:
                self.status_text.append(result.stdout)
            
            self.tags_pushed = True
            self.push_tags_btn.setEnabled(False)
            self.check_all_pushed()
        
        except subprocess.CalledProcessError as e:
            self.status_text.append(f"❌ Push failed: {e.stderr}")
            QMessageBox.critical(self, "Error", f"Failed to push tag:\n{e.stderr}")
    
    def check_all_pushed(self):
        """Check if everything is pushed"""
        if self.commits_pushed and self.tags_pushed:
            self.status_text.append("\n✅ Everything pushed to GitHub!")
            self.next_btn.setEnabled(True)
    
    def get_wizard(self):
        """Get reference to parent wizard"""
        parent = self.parent()
        while parent:
            if isinstance(parent, ReleaseWizard):
                return parent
            parent = parent.parent()
        return None
    
    def get_data(self):
        return {"pushed": self.commits_pushed and self.tags_pushed}


class Step9GitHubReleaseWidget(StepWidget):
    """Step 9: Create GitHub release"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "<h3>Create GitHub Release</h3>"
            "<p>Create the GitHub release and upload distribution files.</p>"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Release type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Release Type:"))
        self.release_type_group = QButtonGroup()
        
        latest_radio = QRadioButton("Latest (production)")
        latest_radio.setChecked(True)
        self.release_type_group.addButton(latest_radio, 1)
        type_layout.addWidget(latest_radio)
        
        prerelease_radio = QRadioButton("Pre-release (beta)")
        self.release_type_group.addButton(prerelease_radio, 2)
        type_layout.addWidget(prerelease_radio)
        
        layout.addLayout(type_layout)
        
        # Files to upload
        files_group = QLabel("<b>Files to Upload:</b>")
        layout.addWidget(files_group)
        
        self.files_list = QListWidget()
        self.files_list.setMaximumHeight(100)
        layout.addWidget(self.files_list)
        
        # Add default files
        if os.path.exists('data/bible_data.sql.gz'):
            self.files_list.addItem('data/bible_data.sql.gz')
        if os.path.exists('data/checksums.txt'):
            self.files_list.addItem('data/checksums.txt')
        
        # Status display
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Create release button
        layout.addStretch()
        self.create_btn = QPushButton("🚀 Create GitHub Release")
        self.create_btn.setStyleSheet("background-color: #FF5722; color: white; padding: 10px; font-weight: bold;")
        self.create_btn.clicked.connect(self.create_release)
        layout.addWidget(self.create_btn)
        
        # Next button (initially disabled)
        self.next_btn = QPushButton("✓ Release Complete!")
        self.next_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.mark_completed)
        layout.addWidget(self.next_btn)
        
        self.release_thread = None
        self.release_url = ""
    
    def create_release(self):
        """Create GitHub release"""
        wizard = self.get_wizard()
        if not wizard:
            return
        
        version = wizard.get_step_data(1).get('version', '')
        notes = wizard.get_step_data(2).get('notes', '')
        
        if not version:
            QMessageBox.warning(self, "No Version", "Version not set")
            return
        
        is_prerelease = self.release_type_group.checkedId() == 2
        
        # Get files to upload
        files_to_upload = []
        for i in range(self.files_list.count()):
            files_to_upload.append(self.files_list.item(i).text())
        
        # Confirm
        file_list = "\n".join([os.path.basename(f) for f in files_to_upload])
        confirm_msg = f"Create GitHub release {version}?\n\n"
        confirm_msg += f"Type: {'Pre-release' if is_prerelease else 'Latest'}\n\n"
        if files_to_upload:
            confirm_msg += f"Files to upload:\n{file_list}"
        
        reply = QMessageBox.question(self, "Confirm Release",
                                    confirm_msg,
                                    QMessageBox.StandardButton.Yes |
                                    QMessageBox.StandardButton.No)
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        self.status_text.clear()
        self.create_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        
        # Create and start release thread
        self.release_thread = GitHubReleaseThread(
            version, notes, is_prerelease, files_to_upload
        )
        
        self.release_thread.progress.connect(self.on_progress)
        self.release_thread.finished.connect(self.on_finished)
        self.release_thread.start()
    
    def on_progress(self, message):
        """Handle progress updates"""
        self.status_text.append(message)
    
    def on_finished(self, success, message, release_url):
        """Handle release completion"""
        self.progress_bar.setVisible(False)
        self.create_btn.setEnabled(True)
        
        if success:
            self.status_text.append(f"\n✅ {message}")
            self.release_url = release_url
            
            if release_url:
                self.status_text.append(f"\n🔗 Release URL: {release_url}")
            
            self.next_btn.setEnabled(True)
            self.create_btn.setEnabled(False)
            
            QMessageBox.information(self, "Success", 
                                   f"{message}\n\n" +
                                   f"Release URL:\n{release_url}")
        else:
            self.status_text.append(f"\n❌ {message}")
            QMessageBox.critical(self, "Release Failed", message)
    
    def get_wizard(self):
        """Get reference to parent wizard"""
        parent = self.parent()
        while parent:
            if isinstance(parent, ReleaseWizard):
                return parent
            parent = parent.parent()
        return None
    
    def get_data(self):
        return {"release_created": self.next_btn.isEnabled(),
                "release_url": self.release_url}


class Step10CompleteWidget(StepWidget):
    """Step 10: Completion"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Success message
        success_label = QLabel(
            "<h2 style='color: #4CAF50;'>✅ Release Complete!</h2>"
            "<p style='font-size: 14px;'>Your release has been published successfully.</p>"
        )
        success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(success_label)
        
        # What's next
        next_steps = QLabel(
            "<h3>What's Next:</h3>"
            "<ol>"
            "<li><b>Visit your GitHub release page</b> to verify everything looks correct</li>"
            "<li><b>Test the installation</b> on a clean system using setup.py</li>"
            "<li><b>Announce the release</b> to your users</li>"
            "<li><b>Monitor</b> for any issues or questions</li>"
            "</ol>"
        )
        next_steps.setWordWrap(True)
        layout.addWidget(next_steps)
        
        # Release URL display
        self.url_label = QLabel()
        self.url_label.setWordWrap(True)
        self.url_label.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
        layout.addWidget(self.url_label)
        
        # Open in browser button
        layout.addStretch()
        self.open_btn = QPushButton("🌐 Open Release in Browser")
        self.open_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-weight: bold;")
        self.open_btn.clicked.connect(self.open_release)
        layout.addWidget(self.open_btn)
        
        # Close button
        close_btn = QPushButton("✓ Close Wizard")
        close_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        close_btn.clicked.connect(self.close_wizard)
        layout.addWidget(close_btn)
        
        # Update URL on show
        QTimer.singleShot(100, self.update_url_display)
    
    def update_url_display(self):
        """Update URL display"""
        wizard = self.get_wizard()
        if wizard:
            release_url = wizard.get_step_data(9).get('release_url', '')
            if release_url:
                self.url_label.setText(f"<b>Release URL:</b><br>{release_url}")
                self.open_btn.setEnabled(True)
            else:
                self.url_label.setText("<i>Release URL not available</i>")
                self.open_btn.setEnabled(False)
    
    def open_release(self):
        """Open release in browser"""
        wizard = self.get_wizard()
        if wizard:
            release_url = wizard.get_step_data(9).get('release_url', '')
            if release_url:
                import webbrowser
                webbrowser.open(release_url)
    
    def close_wizard(self):
        """Close the wizard"""
        wizard = self.get_wizard()
        if wizard:
            wizard.close()
    
    def get_wizard(self):
        """Get reference to parent wizard"""
        parent = self.parent()
        while parent:
            if isinstance(parent, ReleaseWizard):
                return parent
            parent = parent.parent()
        return None


# ============================================================================
# MAIN WIZARD WINDOW
# ============================================================================

class ReleaseWizard(QMainWindow):
    """Main release wizard window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bible Search Lite - Release Wizard")
        self.setGeometry(100, 100, 1400, 900)
        
        # Check if we're in a git repository
        if not self.is_git_repo():
            QMessageBox.critical(self, "Error",
                                "Not a git repository!\n\n" +
                                "Please run this tool from the bible-search-lite directory.")
            sys.exit(1)
        
        # Check GitHub CLI authentication
        is_authenticated, auth_message = self.check_gh_auth()
        if not is_authenticated:
            reply = QMessageBox.warning(self, "GitHub CLI Not Authenticated",
                                       f"{auth_message}\n\n" +
                                       "The wizard will still work for most steps, but you'll need to " +
                                       "authenticate before creating the GitHub release.\n\n" +
                                       "Continue anyway?",
                                       QMessageBox.StandardButton.Yes |
                                       QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.No:
                pass  # Continue
            else:
                sys.exit(0)
        
        self.current_step = 0
        self.step_data = {}
        self.step_widgets = []
        
        self.setup_ui()
    
    def is_git_repo(self):
        """Check if current directory is a git repository"""
        try:
            subprocess.run(['git', 'status'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def check_gh_auth(self):
        """Check if GitHub CLI is installed and authenticated"""
        try:
            result = subprocess.run(['gh', '--version'],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                return False, "GitHub CLI (gh) is not installed"
            
            result = subprocess.run(['gh', 'auth', 'status'],
                                  capture_output=True, text=True)
            
            output = result.stderr
            
            if result.returncode == 0 and '✓' in output:
                for line in output.split('\n'):
                    if 'Logged in to github.com as' in line:
                        return True, line.strip()
                return True, "Authenticated to GitHub"
            else:
                return False, "Not authenticated. Run: gh auth login"
        
        except FileNotFoundError:
            return False, "GitHub CLI (gh) is not installed.\nInstall from: https://cli.github.com/"
        except Exception as e:
            return False, f"Error checking authentication: {e}"
    
    def setup_ui(self):
        """Create the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left panel: Step navigation
        self.create_step_navigation(main_layout)
        
        # Right panel: Content area
        self.create_content_area(main_layout)
        
        # Initialize steps
        self.create_step_widgets()
        self.show_step(0)
    
    def create_step_navigation(self, parent_layout):
        """Create left navigation panel with steps"""
        nav_panel = QFrame()
        nav_panel.setFrameShape(QFrame.Shape.StyledPanel)
        nav_panel.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-right: 2px solid #34495e;
            }
        """)
        nav_panel.setFixedWidth(220)
        
        nav_layout = QVBoxLayout(nav_panel)
        nav_layout.setSpacing(0)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Release Steps")
        title.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                color: white;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(title)
        
        # Step buttons
        self.step_buttons = []
        for step in STEPS:
            btn = self.create_step_button(step)
            self.step_buttons.append(btn)
            nav_layout.addWidget(btn)
        
        nav_layout.addStretch()
        parent_layout.addWidget(nav_panel)
    
    def create_step_button(self, step):
        """Create a step navigation button"""
        btn = QPushButton(f"{step['number']}. {step['short_title']}")
        btn.setCheckable(True)
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 15px 20px;
                background-color: #2c3e50;
                color: #bdc3c7;
                border: none;
                border-left: 4px solid transparent;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #34495e;
                color: white;
            }
            QPushButton:checked {
                background-color: #3498db;
                color: white;
                border-left: 4px solid #2ecc71;
                font-weight: bold;
            }
            QPushButton:disabled {
                color: #7f8c8d;
            }
        """)
        
        btn.clicked.connect(lambda: self.show_step(step['number'] - 1))
        
        # Only first step is enabled initially
        btn.setEnabled(step['number'] == 1)
        
        return btn
    
    def create_content_area(self, parent_layout):
        """Create right content area"""
        content_panel = QWidget()
        content_layout = QVBoxLayout(content_panel)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #3498db;
                border-bottom: 2px solid #2980b9;
            }
        """)
        header_layout = QVBoxLayout(header)
        
        self.step_title = QLabel()
        self.step_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        header_layout.addWidget(self.step_title)
        
        self.step_description = QLabel()
        self.step_description.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                padding: 0px 20px 20px 20px;
            }
        """)
        self.step_description.setWordWrap(True)
        header_layout.addWidget(self.step_description)
        
        content_layout.addWidget(header)
        
        # Content area with scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        
        scroll.setWidget(self.content_widget)
        content_layout.addWidget(scroll)
        
        parent_layout.addWidget(content_panel)
    
    def create_step_widgets(self):
        """Create all step widgets"""
        widget_classes = [
            Step1VersionWidget,
            Step2NotesWidget,
            Step3UpdateFilesWidget,
            Step4ExportDBWidget,
            Step5GitStatusWidget,
            Step6GitCommitWidget,
            Step7GitTagWidget,
            Step8GitPushWidget,
            Step9GitHubReleaseWidget,
            Step10CompleteWidget
        ]
        
        for i, (step_info, widget_class) in enumerate(zip(STEPS, widget_classes)):
            widget = widget_class(step_info)
            widget.step_completed.connect(lambda idx=i: self.on_step_completed(idx))
            self.step_widgets.append(widget)
    
    def show_step(self, step_index):
        """Show a specific step"""
        if step_index < 0 or step_index >= len(STEPS):
            return
        
        # Update current step
        self.current_step = step_index
        
        # Update header
        step_info = STEPS[step_index]
        self.step_title.setText(f"Step {step_info['number']}: {step_info['title']}")
        self.step_description.setText(step_info['description'])
        
        # Update step buttons
        for i, btn in enumerate(self.step_buttons):
            btn.setChecked(i == step_index)
        
        # Clear content area
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
        
        # Add new step widget
        self.content_layout.addWidget(self.step_widgets[step_index])
        self.content_layout.addStretch()
    
    def on_step_completed(self, step_index):
        """Handle step completion"""
        # Save step data
        self.step_data[step_index + 1] = self.step_widgets[step_index].get_data()
        
        # Enable next step
        if step_index + 1 < len(self.step_buttons):
            self.step_buttons[step_index + 1].setEnabled(True)
            # Auto-advance to next step
            self.show_step(step_index + 1)
    
    def get_step_data(self, step_number):
        """Get data from a specific step"""
        return self.step_data.get(step_number, {})


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show wizard
    wizard = ReleaseWizard()
    wizard.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
