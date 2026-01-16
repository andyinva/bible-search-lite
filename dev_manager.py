#!/usr/bin/env python3
"""
Bible Search Lite - Development Manager Tool

A GUI tool for managing GitHub operations and releases.
NOT included in Bible Search Lite distribution - for developers only.

Features:
  • View commit history (development vs production)
  • Create and push commits to GitHub
  • Create version releases for distribution
  • Manage release tags and notes

Author: Andrew Hopkins
"""

import sys
import subprocess
import os
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QListWidget, QLineEdit, QMessageBox, QTabWidget,
                             QSplitter, QGroupBox, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class DevManagerWindow(QMainWindow):
    """Main window for development management tool"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bible Search Lite - Development Manager")
        self.setGeometry(100, 100, 1200, 800)

        # Check if we're in a git repository
        if not self.is_git_repo():
            QMessageBox.critical(self, "Error",
                                "Not a git repository!\n\n" +
                                "Please run this tool from the bible-search-lite directory.")
            sys.exit(1)

        self.setup_ui()
        self.load_data()

    def is_git_repo(self):
        """Check if current directory is a git repository"""
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
        title = QLabel("Development Manager")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Tab 1: Commit Management
        self.commit_tab = self.create_commit_tab()
        tabs.addTab(self.commit_tab, "📝 Commits")

        # Tab 2: Release Management
        self.release_tab = self.create_release_tab()
        tabs.addTab(self.release_tab, "🚀 Releases")

        # Tab 3: History View
        self.history_tab = self.create_history_tab()
        tabs.addTab(self.history_tab, "📊 History")

        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def create_commit_tab(self):
        """Create the commit management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Current branch info
        branch_group = QGroupBox("Current Branch")
        branch_layout = QVBoxLayout(branch_group)
        self.branch_label = QLabel("Loading...")
        branch_layout.addWidget(self.branch_label)
        layout.addWidget(branch_group)

        # Git status
        status_group = QGroupBox("Uncommitted Changes")
        status_layout = QVBoxLayout(status_group)
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        status_layout.addWidget(self.status_text)

        refresh_btn = QPushButton("🔄 Refresh Status")
        refresh_btn.clicked.connect(self.refresh_git_status)
        status_layout.addWidget(refresh_btn)
        layout.addWidget(status_group)

        # Commit creation
        commit_group = QGroupBox("Create Commit")
        commit_layout = QVBoxLayout(commit_group)

        commit_layout.addWidget(QLabel("Commit Message:"))
        self.commit_message = QTextEdit()
        self.commit_message.setMaximumHeight(100)
        self.commit_message.setPlaceholderText("Enter commit message here...\n\nExample:\nFix search highlighting bug\n- Fixed phrase matching\n- Improved performance")
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
        """Create the release management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Current version info
        version_group = QGroupBox("Current Version")
        version_layout = QVBoxLayout(version_group)
        self.version_label = QLabel("Loading...")
        version_layout.addWidget(self.version_label)
        layout.addWidget(version_group)

        # Create new release
        release_group = QGroupBox("Create New Release")
        release_layout = QVBoxLayout(release_group)

        # Version input
        version_input_layout = QHBoxLayout()
        version_input_layout.addWidget(QLabel("Version Tag:"))
        self.version_input = QLineEdit()
        self.version_input.setPlaceholderText("e.g., v1.0.5")
        version_input_layout.addWidget(self.version_input)
        release_layout.addLayout(version_input_layout)

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

        # Create release button
        create_release_btn = QPushButton("🚀 Create Release on GitHub")
        create_release_btn.clicked.connect(self.create_release)
        release_layout.addWidget(create_release_btn)

        layout.addWidget(release_group)

        # Instructions
        instructions = QLabel(
            "ℹ️ Note: This will create a git tag and push it to GitHub.\n" +
            "To upload release files (database, etc.), use the GitHub web interface."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666; padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(instructions)

        return widget

    def create_history_tab(self):
        """Create the history view tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        splitter = QSplitter(Qt.Orientation.Vertical)

        # Development commits
        dev_group = QGroupBox("Development Commits (not yet released)")
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

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh History")
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)

        return widget

    def load_data(self):
        """Load all data from git"""
        self.refresh_git_status()
        self.load_branch_info()
        self.load_version_info()
        self.load_commit_history()
        self.load_releases()

    def refresh_git_status(self):
        """Refresh git status display"""
        try:
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
        """Load current version from VERSION.txt or latest tag"""
        version = "Unknown"

        # Try VERSION.txt first
        if os.path.exists('VERSION.txt'):
            try:
                with open('VERSION.txt', 'r') as f:
                    version = f.read().strip()
            except:
                pass

        # Also get latest git tag
        try:
            result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                latest_tag = result.stdout.strip()
                version = f"{version} (Latest tag: {latest_tag})"
        except:
            pass

        self.version_label.setText(f"Current Version: {version}")

    def load_commit_history(self):
        """Load recent commits not yet in a release"""
        self.dev_commits.clear()
        try:
            # Get commits since last tag
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

    def create_release(self):
        """Create a new release tag"""
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

        try:
            # Create git tag
            subprocess.run(['git', 'tag', '-a', version, '-m', notes], check=True)

            # Push tag to GitHub
            subprocess.run(['git', 'push', 'origin', version], check=True)

            # Update VERSION.txt
            with open('VERSION.txt', 'w') as f:
                f.write(version + '\n')

            self.status_label.setText(f"Status: Release {version} created")
            self.version_input.clear()
            self.release_notes.clear()
            self.load_data()

            QMessageBox.information(self, "Success",
                                  f"Release {version} created and pushed to GitHub!\n\n" +
                                  "Next steps:\n" +
                                  "1. Go to GitHub repository > Releases\n" +
                                  "2. Find your tag and click 'Create release from tag'\n" +
                                  "3. Upload release files (bible_data.sql.gz, checksums.txt)\n" +
                                  "4. Publish the release")

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error",
                               f"Failed to create release:\n{e}")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    window = DevManagerWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
