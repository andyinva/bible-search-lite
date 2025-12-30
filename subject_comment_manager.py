"""
Subject Comment Manager - Window 5 Logic

Manages comments for subject verses with rich-text editing.
"""

from PyQt6.QtWidgets import (QPushButton, QTextEdit, QHBoxLayout,
                              QVBoxLayout, QWidget, QFrame, QLabel, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCharFormat
from bible_search_ui.ui.widgets import SectionWidget


class SubjectCommentManager:
    """
    Manages comments for subject verses (Window 5).
    Handles comment creation, editing, and persistence.
    """

    def __init__(self, db_conn, parent_app):
        """
        Initialize comment manager.

        Args:
            db_conn: SQLite database connection
            parent_app: Reference to main BibleSearchProgram
        """
        self.db_conn = db_conn
        self.parent_app = parent_app

        # State
        self.current_verse_id = None  # DB ID from subject_verses table
        self.editing_mode = False

        # UI components
        self.comments_editor = None
        self.formatting_toolbar = None
        self.add_btn = None
        self.edit_btn = None
        self.save_btn = None
        self.delete_btn = None
        self.close_btn = None

        # Formatting buttons
        self.bold_btn = None
        self.italic_btn = None
        self.underline_btn = None
        self.font_size_combo = None

    def create_ui(self):
        """
        Build the UI for Window 5.

        Returns:
            Tuple of (section_widget, controls_widget)
        """
        # Create controls with solid background
        controls_widget = QWidget()
        controls_widget.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setContentsMargins(5, 5, 5, 5)

        self.add_btn = QPushButton("Add Comment")
        self.add_btn.clicked.connect(self.on_add_comment)
        controls_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.on_edit_comment)
        controls_layout.addWidget(self.edit_btn)

        self.save_btn = QPushButton("Save")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.on_save_comment)
        controls_layout.addWidget(self.save_btn)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.on_delete_comment)
        controls_layout.addWidget(self.delete_btn)

        self.close_btn = QPushButton("Close")
        self.close_btn.setEnabled(False)
        self.close_btn.clicked.connect(self.on_close_comment)
        controls_layout.addWidget(self.close_btn)

        # Create container for toolbar and editor
        comments_container = QWidget()
        comments_container_layout = QVBoxLayout(comments_container)
        comments_container_layout.setContentsMargins(0, 0, 0, 0)
        comments_container_layout.setSpacing(0)

        # Create formatting toolbar (initially hidden)
        self.formatting_toolbar = self.create_formatting_toolbar()
        self.formatting_toolbar.setVisible(False)
        comments_container_layout.addWidget(self.formatting_toolbar)

        # Create QTextEdit for rich text comments
        self.comments_editor = QTextEdit()
        self.comments_editor.setPlaceholderText("Select a verse in Window 4 to add comments...")
        self.comments_editor.setReadOnly(True)
        self.comments_editor.setStyleSheet("background-color: white; padding: 10px;")

        # Wrap in beveled frame
        comments_frame = QFrame()
        comments_frame.setFrameShape(QFrame.Shape.Panel)
        comments_frame.setFrameShadow(QFrame.Shadow.Sunken)
        comments_frame.setLineWidth(3)
        comments_frame.setMidLineWidth(2)
        comments_layout = QVBoxLayout(comments_frame)
        comments_layout.setContentsMargins(0, 0, 0, 0)
        comments_layout.addWidget(self.comments_editor)

        comments_container_layout.addWidget(comments_frame)

        # Create section widget
        section = SectionWidget(
            "5. Subject Verse Comments",
            comments_container,
            controls_widget
        )

        return section, controls_widget

    def create_formatting_toolbar(self):
        """Create a formatting toolbar widget that can be shown/hidden."""
        toolbar_widget = QWidget()
        toolbar_widget.setStyleSheet("background-color: #f5f5f5; padding: 5px;")
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)

        # Bold button
        self.bold_btn = QPushButton("B")
        self.bold_btn.setStyleSheet("font-weight: bold; min-width: 30px; padding: 5px;")
        self.bold_btn.setEnabled(False)
        self.bold_btn.clicked.connect(lambda: self.toggle_format('bold'))
        toolbar_layout.addWidget(self.bold_btn)

        # Italic button
        self.italic_btn = QPushButton("I")
        self.italic_btn.setStyleSheet("font-style: italic; min-width: 30px; padding: 5px;")
        self.italic_btn.setEnabled(False)
        self.italic_btn.clicked.connect(lambda: self.toggle_format('italic'))
        toolbar_layout.addWidget(self.italic_btn)

        # Underline button
        self.underline_btn = QPushButton("U")
        self.underline_btn.setStyleSheet("text-decoration: underline; min-width: 30px; padding: 5px;")
        self.underline_btn.setEnabled(False)
        self.underline_btn.clicked.connect(lambda: self.toggle_format('underline'))
        toolbar_layout.addWidget(self.underline_btn)

        # Font size combo
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["8", "9", "10", "11", "12", "14", "16", "18", "20", "24"])
        self.font_size_combo.setCurrentText("10")
        self.font_size_combo.setMinimumWidth(60)
        self.font_size_combo.setEnabled(False)
        self.font_size_combo.currentTextChanged.connect(self.change_font_size)
        toolbar_layout.addWidget(self.font_size_combo)

        toolbar_layout.addStretch()

        return toolbar_widget

    def load_comment_for_verse(self, verse_db_id):
        """
        Load and display comment for a specific verse.

        Args:
            verse_db_id: Database ID from subject_verses table
        """
        self.current_verse_id = verse_db_id

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT comments FROM subject_verses WHERE id = ?", (verse_db_id,))
            row = cursor.fetchone()

            if row and row['comments']:
                self.comments_editor.setHtml(row['comments'])
                self.edit_btn.setEnabled(True)
                self.delete_btn.setEnabled(True)
            else:
                self.comments_editor.clear()
                self.edit_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)

        except Exception as e:
            print(f"⚠️  Error loading comment: {e}")

    def on_add_comment(self):
        """Start adding a new comment."""
        if not self.current_verse_id:
            self.parent_app.message_label.setText("⚠️  Select a verse first")
            return

        self.comments_editor.clear()
        self.comments_editor.setReadOnly(False)
        self.comments_editor.setFocus()
        self.editing_mode = True
        self.update_button_states()
        self.parent_app.message_label.setText("Adding comment... (Click Save when done)")

    def on_edit_comment(self):
        """Start editing the current comment."""
        if not self.current_verse_id:
            return

        self.comments_editor.setReadOnly(False)
        self.comments_editor.setFocus()
        self.editing_mode = True
        self.update_button_states()
        self.parent_app.message_label.setText("Editing comment... (Click Save when done)")

    def on_save_comment(self):
        """Save the current comment to database."""
        if not self.current_verse_id:
            return

        try:
            comment_html = self.comments_editor.toHtml()

            cursor = self.db_conn.cursor()
            cursor.execute("""
                UPDATE subject_verses
                SET comments = ?, modified_date = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (comment_html, self.current_verse_id))
            self.db_conn.commit()

            self.comments_editor.setReadOnly(True)
            self.editing_mode = False
            self.update_button_states()
            self.parent_app.message_label.setText("✓ Comment saved")

        except Exception as e:
            self.parent_app.message_label.setText(f"⚠️  Error saving comment: {e}")

    def on_delete_comment(self):
        """Delete the current comment."""
        if not self.current_verse_id:
            return

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("""
                UPDATE subject_verses
                SET comments = '', modified_date = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (self.current_verse_id,))
            self.db_conn.commit()

            self.comments_editor.clear()
            self.editing_mode = False
            self.update_button_states()
            self.parent_app.message_label.setText("✓ Comment deleted")

        except Exception as e:
            self.parent_app.message_label.setText(f"⚠️  Error deleting comment: {e}")

    def on_close_comment(self):
        """Cancel editing without saving."""
        # Reload original comment
        if self.current_verse_id:
            self.load_comment_for_verse(self.current_verse_id)

        self.comments_editor.setReadOnly(True)
        self.editing_mode = False
        self.update_button_states()
        self.parent_app.message_label.setText("Editing cancelled")

    def toggle_format(self, format_type):
        """Toggle text formatting (bold, italic, underline)."""
        if self.comments_editor.isReadOnly():
            return

        cursor = self.comments_editor.textCursor()
        format = cursor.charFormat()

        if format_type == 'bold':
            weight = QFont.Weight.Normal if format.fontWeight() == QFont.Weight.Bold else QFont.Weight.Bold
            format.setFontWeight(weight)
        elif format_type == 'italic':
            format.setFontItalic(not format.fontItalic())
        elif format_type == 'underline':
            format.setFontUnderline(not format.fontUnderline())

        cursor.setCharFormat(format)
        self.comments_editor.setTextCursor(cursor)

    def change_font_size(self, size_text):
        """Change font size of selected text."""
        if self.comments_editor.isReadOnly():
            return

        try:
            size = int(size_text)
            cursor = self.comments_editor.textCursor()
            format = cursor.charFormat()
            format.setFontPointSize(size)
            cursor.setCharFormat(format)
            self.comments_editor.setTextCursor(cursor)
        except ValueError:
            pass

    def update_button_states(self):
        """Update button enabled/disabled states based on context."""
        is_editing = self.editing_mode
        has_comment = bool(self.current_verse_id and self.comments_editor.toPlainText())

        self.add_btn.setEnabled(not is_editing)
        self.edit_btn.setEnabled(has_comment and not is_editing)
        self.save_btn.setEnabled(is_editing)
        self.delete_btn.setEnabled(has_comment and not is_editing)
        self.close_btn.setEnabled(is_editing)

        # Formatting toolbar buttons
        self.bold_btn.setEnabled(is_editing)
        self.italic_btn.setEnabled(is_editing)
        self.underline_btn.setEnabled(is_editing)
        self.font_size_combo.setEnabled(is_editing)

        # Show/hide formatting toolbar
        self.formatting_toolbar.setVisible(is_editing)

    def cleanup(self):
        """Clean up resources."""
        pass
