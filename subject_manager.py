"""
Subject Manager - Container for Windows 4 & 5

Manages the lifecycle and visibility of Subject Verses (Window 4) and
Comments (Window 5) as a cohesive, toggleable unit.
"""

import sqlite3
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSplitter
from PyQt6.QtCore import Qt


class SubjectManager:
    """
    Manages Subject Verses (Window 4) and Comments (Window 5) as a unit.
    Can be shown/hidden based on user settings.
    """

    def __init__(self, config_manager, parent_app):
        """
        Initialize the subject manager.

        Args:
            config_manager: ConfigManager instance for settings
            parent_app: Reference to main BibleSearchProgram
        """
        self.config_manager = config_manager
        self.parent_app = parent_app
        self.is_visible = config_manager.load().get('ShowSubjectFeatures', False)

        # Database
        self.db_path = os.path.join(
            os.path.dirname(__file__),
            'database',
            'subjects.db'
        )
        self.db_conn = None

        # Sub-components (lazy loaded)
        self.verse_manager = None
        self.comment_manager = None

        # UI references (set when UI is created)
        self.container_widget = None
        self.subject_section = None  # SectionWidget for Window 4
        self.comments_section = None  # SectionWidget for Window 5

    def initialize_database(self):
        """Initialize database connection and create if needed."""
        try:
            # Create database directory if it doesn't exist
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)

            # Create database if it doesn't exist
            if not os.path.exists(self.db_path):
                print(f"Creating new subjects database: {self.db_path}")
                self._create_database()

            self.db_conn = sqlite3.connect(self.db_path)
            self.db_conn.row_factory = sqlite3.Row
            print(f"✓ Subject manager connected to: {self.db_path}")
            return True
        except Exception as e:
            print(f"⚠️  Subject manager database error: {e}")
            return False

    def _create_database(self):
        """Create subjects database with required schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Subjects table
        cursor.execute("""
            CREATE TABLE subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Subject verses table
        cursor.execute("""
            CREATE TABLE subject_verses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                verse_reference TEXT NOT NULL,
                verse_text TEXT NOT NULL,
                translation TEXT NOT NULL,
                comments TEXT DEFAULT '',
                order_index INTEGER DEFAULT 0,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
                UNIQUE(subject_id, verse_reference, translation)
            )
        """)

        # Create indexes
        cursor.execute("""
            CREATE INDEX idx_subject_verses_subject_id
            ON subject_verses(subject_id)
        """)

        cursor.execute("""
            CREATE INDEX idx_subject_verses_order
            ON subject_verses(subject_id, order_index)
        """)

        cursor.execute("""
            CREATE INDEX idx_subjects_name
            ON subjects(name)
        """)

        conn.commit()
        conn.close()
        print(f"✓ Created subjects database: {self.db_path}")

    def create_ui(self, main_splitter):
        """
        Create the UI for Windows 4 & 5 as a combined unit.

        Args:
            main_splitter: QSplitter where the combined section will be added

        Returns:
            Tuple of (combined_container, None) or (None, None)
        """
        if not self.initialize_database():
            return None, None

        # Import here to avoid circular imports
        from subject_verse_manager import SubjectVerseManager
        from subject_comment_manager import SubjectCommentManager

        # Create sub-managers
        self.verse_manager = SubjectVerseManager(self.db_conn, self.parent_app)
        self.comment_manager = SubjectCommentManager(self.db_conn, self.parent_app)

        # Create UI sections
        self.subject_section, subject_controls = self.verse_manager.create_ui()
        self.comments_section, comment_controls = self.comment_manager.create_ui()

        # Create a combined container widget with vertical splitter
        self.container_widget = QFrame()
        self.container_widget.setFrameShape(QFrame.Shape.StyledPanel)
        self.container_widget.setFrameShadow(QFrame.Shadow.Raised)
        self.container_widget.setLineWidth(3)
        self.container_widget.setMidLineWidth(2)
        # Set gray background for Windows compatibility (matches Linux appearance)
        self.container_widget.setStyleSheet("QFrame { background-color: #e0e0e0; }")

        container_layout = QVBoxLayout(self.container_widget)
        container_layout.setContentsMargins(3, 3, 3, 3)
        container_layout.setSpacing(3)

        # Add title bar with close button
        from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #f0f0f0; padding: 2px;")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(5, 2, 5, 2)
        title_bar_layout.setSpacing(5)

        title_label = QLabel("Subject Features (Windows 4 & 5)")
        title_label.setStyleSheet("font-weight: bold; font-size: 10px; color: #333;")
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(20)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #999;
                border-radius: 3px;
                font-size: 9px;
                font-weight: bold;
                padding: 2px 6px;
                color: #666;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                color: white;
                border: 1px solid #c0392b;
            }
        """)
        close_btn.setToolTip("Close Subject Features (Windows 4 & 5)")
        close_btn.clicked.connect(self.hide)
        title_bar_layout.addWidget(close_btn)

        container_layout.addWidget(title_bar)

        # Create internal splitter for Windows 4 & 5
        internal_splitter = QSplitter(Qt.Orientation.Vertical)
        # Set gray background for splitter handle (Windows compatibility)
        internal_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #c0c0c0;
                height: 3px;
            }
            QSplitter {
                background-color: #e0e0e0;
            }
        """)
        internal_splitter.addWidget(self.subject_section)
        internal_splitter.addWidget(self.comments_section)

        # Restore saved sizes or use defaults
        config = self.config_manager.load()
        saved_sizes = config.get('subject_splitter_sizes', [300, 200])
        internal_splitter.setSizes(saved_sizes)
        print(f"✓ Restored Windows 4 & 5 splitter sizes: {saved_sizes}")

        # Store reference for saving later
        self.internal_splitter = internal_splitter

        container_layout.addWidget(internal_splitter)

        # Add to main splitter
        if self.is_visible:
            main_splitter.addWidget(self.container_widget)

        return self.container_widget, None

    def show(self):
        """Make Windows 4 & 5 visible."""
        if self.container_widget:
            self.container_widget.setVisible(True)
            self.is_visible = True

            # Update toggle button state
            if hasattr(self.parent_app, 'subject_toggle_btn'):
                self.parent_app.subject_toggle_btn.setChecked(True)
                self.parent_app.update_subject_toggle_style(True)

            # Sync Window 4 subject dropdown with Window 3 selection
            if hasattr(self.parent_app, 'reading_subject_combo') and self.verse_manager:
                selected_subject = self.parent_app.reading_subject_combo.currentText().strip()
                if selected_subject:
                    # Set the subject in Window 4's dropdown
                    self.verse_manager.subject_dropdown.setCurrentText(selected_subject)
                    print(f"✓ Synced Window 4 to Window 3 subject: '{selected_subject}'")

            # Save to config
            config = self.config_manager.load()
            config['ShowSubjectFeatures'] = True
            self.config_manager.save(config)

            print("✓ Subject features shown")

    def hide(self):
        """Hide Windows 4 & 5."""
        if self.container_widget:
            self.container_widget.setVisible(False)
            self.is_visible = False

            # Update toggle button state
            if hasattr(self.parent_app, 'subject_toggle_btn'):
                btn = self.parent_app.subject_toggle_btn

                # Block signals to prevent recursive calls
                btn.blockSignals(True)

                # Clear stylesheet first to reset state
                btn.setStyleSheet("")

                # Set to unchecked
                btn.setChecked(False)

                # Re-apply the gray style
                self.parent_app.update_subject_toggle_style(False)

                # Unblock signals
                btn.blockSignals(False)

                # Force visual update
                btn.repaint()

            # Save to config
            config = self.config_manager.load()
            config['ShowSubjectFeatures'] = False
            self.config_manager.save(config)

            print("✓ Subject features hidden")

    def toggle(self):
        """Toggle visibility of Windows 4 & 5."""
        if self.is_visible:
            self.hide()
        else:
            self.show()

    def add_verses_from_selection(self, verse_list, source_window):
        """
        Add selected verses to current subject.
        Called by main app when user clicks "Acquire" button.

        Args:
            verse_list: List of verse dictionaries
            source_window: Source identifier ('search' or 'reading')

        Returns:
            Number of verses added
        """
        if self.verse_manager and self.is_visible:
            return self.verse_manager.add_verses(verse_list)
        return 0

    def get_current_subject(self):
        """Get the currently selected subject name."""
        if self.verse_manager:
            return self.verse_manager.current_subject
        return None

    def cleanup(self):
        """Clean up resources before closing."""
        if self.verse_manager:
            self.verse_manager.cleanup()
        if self.comment_manager:
            self.comment_manager.cleanup()
        if self.db_conn:
            self.db_conn.close()
            print("✓ Subject manager database connection closed")
