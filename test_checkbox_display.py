#!/usr/bin/env python3
"""
Test script to verify checkbox display in VerseItemWidget
Tests the cross-platform checkbox styling with visible checkmark
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from bible_search_ui.ui.widgets import VerseItemWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkbox Display Test")
        self.setGeometry(100, 100, 600, 400)

        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Add test verses with checkboxes
        layout.addWidget(VerseItemWidget(
            verse_id="test1",
            translation="KJV",
            book_abbrev="Gen",
            chapter=1,
            verse_number=1,
            text="In the beginning God created the heaven and the earth."
        ))

        layout.addWidget(VerseItemWidget(
            verse_id="test2",
            translation="NIV",
            book_abbrev="John",
            chapter=3,
            verse_number=16,
            text="For God so loved the world that he gave his one and only Son."
        ))

        layout.addWidget(VerseItemWidget(
            verse_id="test3",
            translation="ESV",
            book_abbrev="Psa",
            chapter=23,
            verse_number=1,
            text="The Lord is my shepherd; I shall not want."
        ))

        # Add button to check which verses are selected
        btn = QPushButton("Print Selected Verses")
        btn.clicked.connect(self.print_selected)
        layout.addWidget(btn)

        layout.addStretch()

    def print_selected(self):
        """Print which checkboxes are checked"""
        print("\n=== Checkbox States ===")
        for i, child in enumerate(self.centralWidget().findChildren(VerseItemWidget)):
            state = "CHECKED" if child.checkbox.isChecked() else "unchecked"
            print(f"Verse {i+1}: {state}")

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()

    print("Checkbox Display Test")
    print("=" * 50)
    print("Instructions:")
    print("1. Try clicking the checkboxes next to each verse")
    print("2. You should see a visible checkmark appear when checked")
    print("3. Click 'Print Selected Verses' to see which are selected")
    print("4. Close the window when done")
    print("=" * 50)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
