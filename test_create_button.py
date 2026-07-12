#!/usr/bin/env python3
"""
Test script for Create button state management
Tests the logic for enabling/disabling and styling the Create button
based on subject dropdown text changes.
"""

import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QLabel
)


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Button State Test")
        self.setGeometry(100, 100, 600, 300)

        # Create in-memory database for testing
        self.db_conn = sqlite3.connect(":memory:")
        self.db_conn.row_factory = sqlite3.Row
        cursor = self.db_conn.cursor()
        cursor.execute("""
            CREATE TABLE subjects (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        """)
        # Add some test subjects
        cursor.execute("INSERT INTO subjects (name) VALUES ('Prayer')")
        cursor.execute("INSERT INTO subjects (name) VALUES ('Faith')")
        cursor.execute("INSERT INTO subjects (name) VALUES ('Love')")
        self.db_conn.commit()

        # Main widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Instructions
        instructions = QLabel(
            "Test Instructions:\n"
            "1. Type a NEW subject name → Button should turn GREEN and be enabled\n"
            "2. Type an EXISTING subject (Prayer, Faith, Love) → Button should be GRAY and disabled\n"
            "3. Clear the text → Button should be GRAY and disabled"
        )
        instructions.setStyleSheet("background-color: #e8f4f8; padding: 10px; border-radius: 5px;")
        layout.addWidget(instructions)

        # Test Area 1: Window 3 style (using parent app's get_button_style)
        layout.addWidget(QLabel("\nWindow 3 (Reading Window) Style:"))
        w3_widget = QWidget()
        w3_layout = QHBoxLayout(w3_widget)

        self.w3_combo = QComboBox()
        self.w3_combo.setEditable(True)
        self.w3_combo.setPlaceholderText("Select or create subject...")
        self.w3_combo.addItems(["Prayer", "Faith", "Love"])
        self.w3_combo.editTextChanged.connect(self.update_w3_button_state)
        w3_layout.addWidget(self.w3_combo)

        self.w3_create_btn = QPushButton("Create")
        self.w3_create_btn.setEnabled(False)
        self.w3_create_btn.setStyleSheet(self.get_button_style(active=False))
        w3_layout.addWidget(self.w3_create_btn)

        self.w3_status = QLabel("Status: Disabled (no text)")
        w3_layout.addWidget(self.w3_status)

        layout.addWidget(w3_widget)

        # Test Area 2: Window 4 style (using local styles)
        layout.addWidget(QLabel("\nWindow 4 (Subject Verses Window) Style:"))
        w4_widget = QWidget()
        w4_layout = QHBoxLayout(w4_widget)

        self.w4_combo = QComboBox()
        self.w4_combo.setEditable(True)
        self.w4_combo.setPlaceholderText("Select or create subject...")
        self.w4_combo.addItems(["Prayer", "Faith", "Love"])
        self.w4_combo.editTextChanged.connect(self.update_w4_button_state)
        w4_layout.addWidget(self.w4_combo)

        self.w4_create_btn = QPushButton("Create")
        self.w4_create_btn.setEnabled(False)
        self.w4_create_btn.setStyleSheet(self.get_gray_style())
        w4_layout.addWidget(self.w4_create_btn)

        self.w4_status = QLabel("Status: Disabled (no text)")
        w4_layout.addWidget(self.w4_status)

        layout.addWidget(w4_widget)

        layout.addStretch()

    def get_button_style(self, active=False):
        """Window 3 button style (matches bible_search_lite.py)"""
        if active:
            return """
                QPushButton {
                    background-color: #4CAF50;
                    border: 2px solid #2E7D32;
                    padding: 4px 8px;
                    border-radius: 2px;
                    min-width: 50px;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #e0e0e0;
                    border: 1px solid #999;
                    padding: 4px 8px;
                    border-radius: 2px;
                    min-width: 50px;
                    color: #000000;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                    color: #000000;
                }
                QPushButton:pressed {
                    background-color: #c0c0c0;
                    color: #000000;
                }
                QPushButton:disabled {
                    background-color: #f0f0f0;
                    color: #999999;
                    border: 1px solid #ccc;
                }
            """

    def get_gray_style(self):
        """Window 4 gray style"""
        return """
            QPushButton {
                background-color: #f0f0f0;
                color: #999999;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 4px 8px;
            }
        """

    def get_green_style(self):
        """Window 4 green style"""
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #2E7D32;
                border-radius: 3px;
                padding: 4px 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """

    def update_w3_button_state(self, text):
        """Update Window 3 Create button state (matches bible_search_lite.py)"""
        text = text.strip()

        if not text:
            self.w3_create_btn.setEnabled(False)
            self.w3_create_btn.setStyleSheet(self.get_button_style(active=False))
            self.w3_status.setText("Status: Disabled (no text)")
            return

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT id FROM subjects WHERE name = ?", (text,))
            exists = cursor.fetchone() is not None

            if exists:
                self.w3_create_btn.setEnabled(False)
                self.w3_create_btn.setStyleSheet(self.get_button_style(active=False))
                self.w3_status.setText(f"Status: Disabled ('{text}' exists)")
            else:
                self.w3_create_btn.setEnabled(True)
                self.w3_create_btn.setStyleSheet(self.get_button_style(active=True))
                self.w3_status.setText(f"Status: ENABLED ('{text}' is NEW)")
        except Exception as e:
            self.w3_create_btn.setEnabled(False)
            self.w3_create_btn.setStyleSheet(self.get_button_style(active=False))
            self.w3_status.setText(f"Status: Error - {e}")

    def update_w4_button_state(self, text):
        """Update Window 4 Create button state (matches subject_verse_manager.py)"""
        text = text.strip()

        if not text:
            self.w4_create_btn.setEnabled(False)
            self.w4_create_btn.setStyleSheet(self.get_gray_style())
            self.w4_status.setText("Status: Disabled (no text)")
            return

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT id FROM subjects WHERE name = ?", (text,))
            exists = cursor.fetchone() is not None

            if exists:
                self.w4_create_btn.setEnabled(False)
                self.w4_create_btn.setStyleSheet(self.get_gray_style())
                self.w4_status.setText(f"Status: Disabled ('{text}' exists)")
            else:
                self.w4_create_btn.setEnabled(True)
                self.w4_create_btn.setStyleSheet(self.get_green_style())
                self.w4_status.setText(f"Status: ENABLED ('{text}' is NEW)")
        except Exception as e:
            self.w4_create_btn.setEnabled(False)
            self.w4_create_btn.setStyleSheet(self.get_gray_style())
            self.w4_status.setText(f"Status: Error - {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
