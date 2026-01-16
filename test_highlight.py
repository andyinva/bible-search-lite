#!/usr/bin/env python3
"""Test gray highlighting in isolation"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QColor, QBrush, QPalette

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        layout = QHBoxLayout(self)
        label = QLabel("Test verse text")
        layout.addWidget(label)

        # Set gray background using all three methods
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(224, 224, 224))
        self.setPalette(palette)

        self.setStyleSheet("""
            QWidget {
                background-color: #e0e0e0;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Highlight Test")
        self.setGeometry(100, 100, 600, 400)

        list_widget = QListWidget()
        self.setCentralWidget(list_widget)

        # Add 5 test items
        for i in range(5):
            item = QListWidgetItem(list_widget)
            widget = TestWidget()
            item.setSizeHint(widget.sizeHint())
            list_widget.setItemWidget(item, widget)

            # Set gray background on item 2 using QListWidgetItem.setBackground()
            if i == 2:
                item.setBackground(QBrush(QColor(224, 224, 224)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
