"""
Export Dialog - Comprehensive verse export with multiple options

Allows exporting from:
- Search results (Window 2)
- Reading window (Window 3)
- Subject verses (Window 4) with optional comments
- Messages database

Formats:
- CSV (Comma delimited)
- RTF (Rich Text Format)

Options:
- Selected verses only or all verses
- Include comments (for subject export)
- Save to downloads folder or custom location
- Optional printer output
"""

import os
import csv
from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QRadioButton, QCheckBox, QButtonGroup, QFileDialog,
    QGroupBox, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument


class ExportDialog(QDialog):
    """Dialog for configuring and executing verse exports"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setWindowTitle("Export Verses")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        # Create downloads folder if it doesn't exist
        self.downloads_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'downloads'
        )
        os.makedirs(self.downloads_folder, exist_ok=True)

        self.setup_ui()

    def setup_ui(self):
        """Set up the dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Title
        title_label = QLabel("Export Verses")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Source selection
        source_group = QGroupBox("Export Source")
        source_layout = QVBoxLayout()

        self.source_group = QButtonGroup(self)

        self.radio_search = QRadioButton("Search Results (Window 2)")
        self.radio_reading = QRadioButton("Reading Window (Window 3)")
        self.radio_subject = QRadioButton("Subject Verses (Window 4)")
        self.radio_messages = QRadioButton("Messages Database")

        self.source_group.addButton(self.radio_search, 1)
        self.source_group.addButton(self.radio_reading, 2)
        self.source_group.addButton(self.radio_subject, 3)
        self.source_group.addButton(self.radio_messages, 4)

        self.radio_search.setChecked(True)

        source_layout.addWidget(self.radio_search)
        source_layout.addWidget(self.radio_reading)
        source_layout.addWidget(self.radio_subject)
        source_layout.addWidget(self.radio_messages)

        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        # Selection options
        selection_group = QGroupBox("Selection")
        selection_layout = QVBoxLayout()

        self.selection_group = QButtonGroup(self)

        self.radio_selected = QRadioButton("Selected verses only (checked)")
        self.radio_all = QRadioButton("All verses in window/subject")

        self.selection_group.addButton(self.radio_selected, 1)
        self.selection_group.addButton(self.radio_all, 2)

        self.radio_selected.setChecked(True)

        selection_layout.addWidget(self.radio_selected)
        selection_layout.addWidget(self.radio_all)

        selection_group.setLayout(selection_layout)
        layout.addWidget(selection_group)

        # Additional options
        options_group = QGroupBox("Additional Options")
        options_layout = QVBoxLayout()

        self.check_include_comments = QCheckBox("Include comments (for Subject export)")
        self.check_include_comments.setEnabled(False)  # Only enabled for subject export

        options_layout.addWidget(self.check_include_comments)

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Format selection
        format_group = QGroupBox("Export Format")
        format_layout = QVBoxLayout()

        self.format_group = QButtonGroup(self)

        self.radio_csv = QRadioButton("CSV (Comma delimited)")
        self.radio_rtf = QRadioButton("RTF (Rich Text Format)")

        self.format_group.addButton(self.radio_csv, 1)
        self.format_group.addButton(self.radio_rtf, 2)

        self.radio_csv.setChecked(True)

        format_layout.addWidget(self.radio_csv)
        format_layout.addWidget(self.radio_rtf)

        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        # File location
        location_group = QGroupBox("Save Location")
        location_layout = QVBoxLayout()

        # File path display
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setText(self.downloads_folder)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.on_browse_clicked)

        path_layout.addWidget(QLabel("Folder:"))
        path_layout.addWidget(self.path_edit, 1)
        path_layout.addWidget(browse_btn)

        location_layout.addLayout(path_layout)

        # Reset to default button
        reset_btn = QPushButton("Reset to Default (downloads)")
        reset_btn.clicked.connect(self.reset_to_default_path)
        location_layout.addWidget(reset_btn)

        location_group.setLayout(location_layout)
        layout.addWidget(location_group)

        # Action buttons
        button_layout = QHBoxLayout()

        export_file_btn = QPushButton("Export to File")
        export_file_btn.clicked.connect(self.on_export_to_file)

        export_print_btn = QPushButton("Send to Printer")
        export_print_btn.clicked.connect(self.on_export_to_printer)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(export_file_btn)
        button_layout.addWidget(export_print_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        # Connect source radio to enable/disable comments checkbox
        self.radio_subject.toggled.connect(self.on_source_changed)

    def on_source_changed(self, checked):
        """Enable/disable comments checkbox based on source selection"""
        if checked:
            self.check_include_comments.setEnabled(True)
        else:
            self.check_include_comments.setEnabled(False)
            self.check_include_comments.setChecked(False)

    def on_browse_clicked(self):
        """Open folder browser to select export location"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Export Folder",
            self.path_edit.text()
        )

        if folder:
            self.path_edit.setText(folder)

    def reset_to_default_path(self):
        """Reset export path to default downloads folder"""
        self.path_edit.setText(self.downloads_folder)

    def get_verses_to_export(self):
        """Get verses based on selected source and selection option"""
        verses = []
        source_name = ""

        # Determine source
        if self.radio_search.isChecked():
            source_name = "Search Results"
            if self.radio_selected.isChecked():
                verse_ids = self.parent_app.verse_lists['search'].get_selected_verses()
                for verse_id in verse_ids:
                    if verse_id in self.parent_app.verse_lists['search'].verse_items:
                        _, widget = self.parent_app.verse_lists['search'].verse_items[verse_id]
                        verses.append({
                            # Honor the Settings toggle for the 3-letter
                            # translation code in the reference
                            'reference': widget.get_verse_reference(
                                getattr(self.parent_app, 'include_translation_code', True)),
                            'text': widget.text,
                            'comment': None
                        })
            else:  # All verses
                for verse_id, (_, widget) in self.parent_app.verse_lists['search'].verse_items.items():
                    verses.append({
                        # Honor the Settings toggle for the 3-letter
                        # translation code in the reference
                        'reference': widget.get_verse_reference(
                            getattr(self.parent_app, 'include_translation_code', True)),
                        'text': widget.text,
                        'comment': None
                    })

        elif self.radio_reading.isChecked():
            source_name = "Reading Window"
            if self.radio_selected.isChecked():
                verse_ids = self.parent_app.verse_lists['reading'].get_selected_verses()
                for verse_id in verse_ids:
                    if verse_id in self.parent_app.verse_lists['reading'].verse_items:
                        _, widget = self.parent_app.verse_lists['reading'].verse_items[verse_id]
                        verses.append({
                            # Honor the Settings toggle for the 3-letter
                            # translation code in the reference
                            'reference': widget.get_verse_reference(
                                getattr(self.parent_app, 'include_translation_code', True)),
                            'text': widget.text,
                            'comment': None
                        })
            else:  # All verses
                for verse_id, (_, widget) in self.parent_app.verse_lists['reading'].verse_items.items():
                    verses.append({
                        # Honor the Settings toggle for the 3-letter
                        # translation code in the reference
                        'reference': widget.get_verse_reference(
                            getattr(self.parent_app, 'include_translation_code', True)),
                        'text': widget.text,
                        'comment': None
                    })

        elif self.radio_subject.isChecked():
            source_name = "Subject Verses"
            if hasattr(self.parent_app, 'subject_manager') and self.parent_app.subject_manager:
                subject_name = self.parent_app.subject_manager.get_current_subject()
                if subject_name:
                    source_name = f"Subject: {subject_name}"
                    verses = self.get_subject_verses(subject_name)
                else:
                    QMessageBox.warning(self, "No Subject Selected", "Please select a subject in Window 4 first.")
                    return None, None
            else:
                QMessageBox.warning(self, "Subject Features Not Available", "Windows 4 & 5 must be open to export subject verses.")
                return None, None

        elif self.radio_messages.isChecked():
            source_name = "Messages Database"
            verses = self.get_messages_from_database()

        if not verses:
            QMessageBox.warning(self, "No Verses to Export", "There are no verses to export with the current selection.")
            return None, None

        return verses, source_name

    def get_book_order_map(self):
        """
        Build a {book abbreviation: canonical position} lookup table.

        The order_index comes from the books table in the main Bible
        database (bibles.db), so Genesis maps to 1, Exodus to 2, and so
        on.  This map is what lets us sort subject verses into true
        biblical order, since subject_verses only stores a text reference
        like "Gen 37:32".

        Returns:
            dict: abbreviation -> order_index (empty dict on failure)
        """
        book_order = {}
        try:
            import sqlite3
            bible_db_path = self.parent_app.search_controller.bible_search.database_path
            bible_conn = sqlite3.connect(bible_db_path)
            bible_cursor = bible_conn.cursor()
            bible_cursor.execute("SELECT abbreviation, order_index FROM books")
            book_order = {row[0]: row[1] for row in bible_cursor.fetchall()}
            bible_conn.close()
        except Exception as e:
            print(f"Error loading book order: {e}")
        return book_order

    @staticmethod
    def parse_verse_reference(verse_reference):
        """
        Split a stored reference like "Gen 37:32" or "2Ki 21:15" into
        its parts.

        Returns:
            tuple: (book_abbrev, chapter, verse) — chapter/verse as ints,
                   or (reference, 0, 0) if the reference cannot be parsed
        """
        try:
            # The book abbreviation is everything before the LAST space,
            # the "chapter:verse" part is everything after it
            book, chap_verse = verse_reference.rsplit(' ', 1)
            chapter_str, verse_str = chap_verse.split(':', 1)
            return book, int(chapter_str), int(verse_str)
        except (ValueError, AttributeError):
            # Unparseable reference — sort it to the end rather than crash
            return verse_reference, 0, 0

    def get_subject_verses(self, subject_name):
        """
        Get verses from the subject database, optionally with comments.

        The verses are returned sorted into biblical order (book, then
        chapter, then verse) no matter what order they were added to the
        subject in.  Previously this method sorted by database row ID
        (insertion order) and also queried columns (book/chapter/verse)
        that do not exist in subjects.db, so subject exports either came
        out scrambled or empty.
        """
        verses = []
        include_comments = self.check_include_comments.isChecked()

        try:
            if hasattr(self.parent_app, 'subject_manager') and self.parent_app.subject_manager:
                db_conn = self.parent_app.subject_manager.db_conn
                cursor = db_conn.cursor()

                # Get subject ID
                cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
                result = cursor.fetchone()
                if not result:
                    return verses

                subject_id = result[0]

                # Get the rows for this subject.  The real subjects.db
                # schema stores a text reference ("Gen 1:1"), the verse
                # text, the translation, and a comments column.
                if self.radio_selected.isChecked() and hasattr(self.parent_app.subject_manager, 'verse_manager'):
                    # Export only the verses checked in Window 4
                    selected_ids = self.parent_app.subject_manager.verse_manager.get_selected_verse_ids()
                    if not selected_ids:
                        return verses

                    placeholders = ','.join('?' * len(selected_ids))
                    query = f"""
                        SELECT id, verse_reference, verse_text, translation, comments
                        FROM subject_verses
                        WHERE subject_id = ? AND id IN ({placeholders})
                    """
                    cursor.execute(query, [subject_id] + selected_ids)
                else:
                    # Export all verses in the subject
                    cursor.execute("""
                        SELECT id, verse_reference, verse_text, translation, comments
                        FROM subject_verses
                        WHERE subject_id = ?
                    """, (subject_id,))

                rows = cursor.fetchall()

                # --- Sort into biblical order -------------------------
                # Build the canonical book-order lookup once, then sort
                # by (book position, chapter, verse number).  Unknown
                # books sort to the end (position 999).
                book_order = self.get_book_order_map()

                def biblical_sort_key(row):
                    book, chapter, verse_num = self.parse_verse_reference(row[1])
                    return (book_order.get(book, 999), chapter, verse_num)

                rows = sorted(rows, key=biblical_sort_key)
                # ------------------------------------------------------

                # Check once whether the newer subject_comments table
                # exists; older databases keep comments in a column on
                # subject_verses instead.
                cursor.execute("""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name='subject_comments'
                """)
                has_comments_table = cursor.fetchone() is not None

                for row in rows:
                    verse_id = row[0]
                    # Honor the Settings toggle: append the 3-letter
                    # translation code only when the user wants it
                    if getattr(self.parent_app, 'include_translation_code', True):
                        reference = f"{row[1]} ({row[3]})"  # e.g. "Gen 1:1 (KJV)"
                    else:
                        reference = row[1]                  # e.g. "Gen 1:1"
                    text = row[2]

                    comment = None
                    if include_comments:
                        if has_comments_table:
                            # New schema: comments live in their own table
                            cursor.execute("""
                                SELECT comment
                                FROM subject_comments
                                WHERE subject_id = ? AND verse_id = ?
                            """, (subject_id, verse_id))
                            comment_row = cursor.fetchone()
                            if comment_row and comment_row[0]:
                                comment = comment_row[0]
                        else:
                            # Old schema: comments column on the verse row
                            if row[4]:
                                comment = row[4]

                    verses.append({
                        'reference': reference,
                        'text': text,
                        'comment': comment
                    })

        except Exception as e:
            print(f"Error getting subject verses: {e}")

        return verses

    def get_messages_from_database(self):
        """Get all messages from the messages database"""
        verses = []

        try:
            # Messages are stored in the main message window
            if hasattr(self.parent_app, 'message_label'):
                # For now, just export the current message
                current_message = self.parent_app.message_label.text()
                if current_message:
                    verses.append({
                        'reference': 'Message',
                        'text': current_message,
                        'comment': None
                    })
        except Exception as e:
            print(f"Error getting messages: {e}")

        return verses

    def export_to_csv(self, verses, source_name, filepath):
        """Export verses to CSV format"""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Reference', 'Text', 'Comment']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({
                    'Reference': f'Source: {source_name}',
                    'Text': f'Exported: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                    'Comment': ''
                })
                writer.writerow({'Reference': '', 'Text': '', 'Comment': ''})  # Blank line

                for verse in verses:
                    writer.writerow({
                        'Reference': verse['reference'],
                        'Text': verse['text'],
                        'Comment': verse.get('comment', '') or ''
                    })

            return True
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export CSV: {e}")
            return False

    def export_to_rtf(self, verses, source_name, filepath):
        """Export verses to RTF format"""
        try:
            rtf_content = []
            rtf_content.append(r'{\rtf1\ansi\deff0')
            rtf_content.append(r'{\fonttbl{\f0 Times New Roman;}}')
            rtf_content.append(r'\f0\fs24')

            # Header
            rtf_content.append(r'\b ')
            rtf_content.append(f'Source: {source_name}')
            rtf_content.append(r'\b0\par')
            rtf_content.append(f'Exported: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            rtf_content.append(r'\par\par')

            # Verses
            for verse in verses:
                # Reference (bold)
                rtf_content.append(r'\b ')
                rtf_content.append(self.escape_rtf(verse['reference']))
                rtf_content.append(r'\b0\par')

                # Text
                rtf_content.append(self.escape_rtf(verse['text']))
                rtf_content.append(r'\par')

                # Comment (if present)
                if verse.get('comment'):
                    rtf_content.append(r'\i Comment: ')
                    rtf_content.append(self.escape_rtf(verse['comment']))
                    rtf_content.append(r'\i0\par')

                rtf_content.append(r'\par')  # Blank line between verses

            rtf_content.append(r'}')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(''.join(rtf_content))

            return True
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export RTF: {e}")
            return False

    def escape_rtf(self, text):
        """Escape special characters for RTF format"""
        if not text:
            return ''
        text = text.replace('\\', '\\\\')
        text = text.replace('{', '\\{')
        text = text.replace('}', '\\}')
        return text

    def on_export_to_file(self):
        """Export verses to file"""
        verses, source_name = self.get_verses_to_export()

        if not verses:
            return

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source_slug = source_name.replace(' ', '_').replace(':', '')

        if self.radio_csv.isChecked():
            extension = 'csv'
        else:
            extension = 'rtf'

        filename = f"{source_slug}_{timestamp}.{extension}"
        filepath = os.path.join(self.path_edit.text(), filename)

        # Export based on format
        success = False
        if self.radio_csv.isChecked():
            success = self.export_to_csv(verses, source_name, filepath)
        else:
            success = self.export_to_rtf(verses, source_name, filepath)

        if success:
            QMessageBox.information(
                self,
                "Export Complete",
                f"Successfully exported {len(verses)} verse(s) to:\n{filepath}"
            )
            self.accept()

    def on_export_to_printer(self):
        """Export verses to printer"""
        verses, source_name = self.get_verses_to_export()

        if not verses:
            return

        # Create print document
        document = QTextDocument()

        # Build HTML content
        html_parts = []
        html_parts.append('<html><body>')
        html_parts.append(f'<h2>Source: {source_name}</h2>')
        html_parts.append(f'<p>Exported: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>')
        html_parts.append('<hr>')

        for verse in verses:
            html_parts.append(f'<p><b>{verse["reference"]}</b><br>')
            html_parts.append(f'{verse["text"]}</p>')

            if verse.get('comment'):
                html_parts.append(f'<p><i>Comment: {verse["comment"]}</i></p>')

            html_parts.append('<br>')

        html_parts.append('</body></html>')

        document.setHtml(''.join(html_parts))

        # Show print dialog
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            document.print(printer)
            QMessageBox.information(
                self,
                "Print Complete",
                f"Successfully sent {len(verses)} verse(s) to printer"
            )
            self.accept()
