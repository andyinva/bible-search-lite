"""
Subject Verse Manager - Window 4 Logic

Manages subject creation, verse collection, and display.
"""

import sqlite3
from PyQt6.QtWidgets import (QPushButton, QComboBox, QHBoxLayout,
                              QVBoxLayout, QWidget, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt
from bible_search_ui.ui.widgets import VerseListWidget, SectionWidget


class SubjectVerseManager:
    """
    Manages subject verses (Window 4).
    Handles subject creation, verse collection, and display.
    """

    def __init__(self, db_conn, parent_app):
        """
        Initialize subject verse manager.

        Args:
            db_conn: SQLite database connection
            parent_app: Reference to main BibleSearchProgram
        """
        self.db_conn = db_conn
        self.parent_app = parent_app

        # State
        self.current_subject = None
        self.current_subject_id = None

        # UI components (created in create_ui)
        self.subject_dropdown = None
        self.subject_verse_list = None
        self.create_btn = None
        self.acquire_btn = None
        self.delete_btn = None
        self.rename_btn = None
        self.delete_subject_btn = None
        self.clear_subject_btn = None

    def create_ui(self):
        """
        Build the UI for Window 4.

        Returns:
            Tuple of (section_widget, controls_widget)
        """
        # Create controls with solid background
        controls_widget = QWidget()
        controls_widget.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setContentsMargins(5, 5, 5, 5)

        # Subject dropdown
        self.subject_dropdown = QComboBox()
        self.subject_dropdown.setEditable(True)
        self.subject_dropdown.setPlaceholderText("Select or create subject...")
        self.subject_dropdown.currentTextChanged.connect(self.on_subject_selected)

        # Style dropdown for visibility on all platforms
        self.subject_dropdown.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid #999;
                padding: 4px 8px;
                border-radius: 2px;
                min-width: 150px;
            }
            QComboBox:editable {
                background-color: white;
                color: black;
            }
            QComboBox:hover {
                border: 1px solid #666;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #555;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #0078d4;
                selection-color: white;
                border: 1px solid #999;
            }
            QLineEdit {
                background-color: white;
                color: black;
            }
        """)

        controls_layout.addWidget(self.subject_dropdown)

        # Button style for cross-platform consistency
        button_style = """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #999999;
                border-radius: 3px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #e6f2ff;
                border: 1px solid #0078d4;
            }
            QPushButton:disabled {
                background-color: #f0f0f0;
                color: #999999;
                border: 1px solid #cccccc;
            }
        """

        # Create button
        self.create_btn = QPushButton("Create")
        self.create_btn.setStyleSheet(button_style)
        self.create_btn.clicked.connect(self.on_create_subject)
        controls_layout.addWidget(self.create_btn)

        # Acquire button
        self.acquire_btn = QPushButton("Acquire")
        self.acquire_btn.setStyleSheet(button_style)
        self.acquire_btn.setEnabled(False)
        self.acquire_btn.clicked.connect(self.on_acquire_verses)
        controls_layout.addWidget(self.acquire_btn)

        # Delete (verses) button
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet(button_style)
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.on_delete_verses)
        controls_layout.addWidget(self.delete_btn)

        # Rename button
        self.rename_btn = QPushButton("Rename")
        self.rename_btn.setStyleSheet(button_style)
        self.rename_btn.setEnabled(False)
        self.rename_btn.clicked.connect(self.on_rename_subject)
        controls_layout.addWidget(self.rename_btn)

        # Delete Subject button
        self.delete_subject_btn = QPushButton("Delete Subject")
        self.delete_subject_btn.setStyleSheet(button_style)
        self.delete_subject_btn.setEnabled(False)
        self.delete_subject_btn.clicked.connect(self.on_delete_subject)
        controls_layout.addWidget(self.delete_subject_btn)

        # Clear Subject button
        self.clear_subject_btn = QPushButton("Clear Subject")
        self.clear_subject_btn.setStyleSheet(button_style)
        self.clear_subject_btn.setEnabled(False)
        self.clear_subject_btn.clicked.connect(self.on_clear_subject)
        controls_layout.addWidget(self.clear_subject_btn)

        # Create verse list
        self.subject_verse_list = VerseListWidget(window_id='subject')
        self.subject_verse_list.verse_navigation_requested.connect(
            self.on_subject_verse_clicked
        )
        self.subject_verse_list.selection_changed.connect(
            self.on_subject_selection_changed
        )

        # Register with parent app
        self.parent_app.verse_lists['subject'] = self.subject_verse_list
        self.parent_app.selection_manager.register_window("subject", self.subject_verse_list)

        # Create section widget
        section = SectionWidget(
            "4. Subject Verses",
            self.subject_verse_list,
            controls_widget,
            main_window=self.parent_app
        )

        # Load subjects
        self.load_subjects()

        return section, controls_widget

    def load_subjects(self):
        """Load all subjects from database into dropdown."""
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT id, name FROM subjects ORDER BY name")
            subjects = cursor.fetchall()

            self.subject_dropdown.clear()
            self.subject_dropdown.addItem("")  # Empty option

            for subject in subjects:
                self.subject_dropdown.addItem(subject['name'])

            print(f"✓ Loaded {len(subjects)} subject(s) into dropdown")

        except Exception as e:
            print(f"⚠️  Error loading subjects: {e}")

    def on_subject_selected(self):
        """Handle subject selection from dropdown."""
        subject_name = self.subject_dropdown.currentText().strip()

        if not subject_name:
            self.current_subject = None
            self.current_subject_id = None
            self.subject_verse_list.clear_verses()
            self.update_button_states()
            return

        # Get subject ID
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
            result = cursor.fetchone()

            if result:
                self.current_subject = subject_name
                self.current_subject_id = result['id']
                self.load_subject_verses()
                self.update_button_states()
                # Update Acquire button based on selections in Windows 2/3
                if hasattr(self.parent_app, 'update_subject_acquire_button'):
                    self.parent_app.update_subject_acquire_button()
                # Sync to Window 3's subject dropdown
                if hasattr(self.parent_app, 'reading_subject_combo'):
                    self.parent_app.reading_subject_combo.setCurrentText(subject_name)
            else:
                self.current_subject = None
                self.current_subject_id = None
                self.update_button_states()
                # Update Acquire button based on selections in Windows 2/3
                if hasattr(self.parent_app, 'update_subject_acquire_button'):
                    self.parent_app.update_subject_acquire_button()

        except Exception as e:
            print(f"⚠️  Error selecting subject: {e}")

    def on_create_subject(self):
        """Create a new subject from dropdown text."""
        subject_name = self.subject_dropdown.currentText().strip()

        if not subject_name:
            self.parent_app.message_label.setText("⚠️  Enter a subject name")
            return

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("INSERT INTO subjects (name) VALUES (?)", (subject_name,))
            self.db_conn.commit()
            subject_id = cursor.lastrowid

            self.current_subject = subject_name
            self.current_subject_id = subject_id

            self.load_subjects()
            self.subject_dropdown.setCurrentText(subject_name)
            self.update_button_states()  # Enable buttons

            # Also update Window 3's subject dropdown
            if hasattr(self.parent_app, 'load_subjects_for_reading'):
                self.parent_app.load_subjects_for_reading()

            self.parent_app.message_label.setText(f"✓ Created subject: {subject_name}")

        except sqlite3.IntegrityError:
            self.parent_app.message_label.setText(f"⚠️  Subject '{subject_name}' already exists")
        except Exception as e:
            self.parent_app.message_label.setText(f"⚠️  Error creating subject: {e}")

    def on_acquire_verses(self):
        """Acquire checked verses from Windows 2 & 3."""
        print(f"🔵 Acquire button clicked in Window 4")

        # Check if Window 4 has a subject selected, otherwise use Window 3's subject
        if not self.current_subject_id:
            # Try to use Window 3's subject selection
            subject_name = self.parent_app.reading_subject_combo.currentText().strip()
            if not subject_name:
                self.parent_app.message_label.setText("⚠️  Select a subject first (in Window 3 or Window 4)")
                print(f"❌ No subject selected in either Window 3 or Window 4")
                return

            # Find or create the subject from Window 3's selection
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,))
                result = cursor.fetchone()

                if result:
                    subject_id = result['id']
                    print(f"✓ Using subject from Window 3: {subject_name} (ID: {subject_id})")
                else:
                    # Create new subject
                    cursor.execute("INSERT INTO subjects (name) VALUES (?)", (subject_name,))
                    self.db_conn.commit()
                    subject_id = cursor.lastrowid
                    print(f"✓ Created new subject from Window 3: {subject_name} (ID: {subject_id})")
                    self.load_subjects()  # Refresh dropdown

                # Temporarily use this subject for this operation
                temp_subject_id = subject_id
                temp_subject_name = subject_name
            except Exception as e:
                self.parent_app.message_label.setText(f"⚠️  Error accessing subject: {e}")
                print(f"❌ Error accessing subject: {e}")
                return
        else:
            temp_subject_id = self.current_subject_id
            temp_subject_name = self.current_subject

        # Get checked verses from Windows 2 & 3
        search_verses = self.parent_app.verse_lists['search'].get_selected_verses()
        reading_verses = self.parent_app.verse_lists['reading'].get_selected_verses()

        print(f"📊 Found {len(search_verses)} verses in Window 2, {len(reading_verses)} verses in Window 3")

        all_verse_ids = search_verses + reading_verses

        if not all_verse_ids:
            self.parent_app.message_label.setText("⚠️  No verses selected")
            print(f"❌ No verses selected in either window")
            return

        # Add verses to the subject (either from Window 4 or Window 3)
        added_count = self.add_verses_to_subject(all_verse_ids, temp_subject_id)

        # Uncheck verses
        self.parent_app.verse_lists['search'].select_none()
        self.parent_app.verse_lists['reading'].select_none()

        self.parent_app.message_label.setText(
            f"✓ Added {added_count} verse(s) to {temp_subject_name}"
        )

        # If we used Window 3's subject and Window 4 is showing, refresh it
        if not self.current_subject_id and self.current_subject == temp_subject_name:
            self.load_subject_verses()

    def add_verses_to_subject(self, verse_ids, subject_id):
        """
        Add verses to a specific subject.

        Args:
            verse_ids: List of verse IDs to add
            subject_id: Subject ID to add verses to

        Returns:
            Number of verses added
        """
        if not subject_id:
            return 0

        added_count = 0

        try:
            cursor = self.db_conn.cursor()

            # Get current max order_index
            cursor.execute(
                "SELECT MAX(order_index) FROM subject_verses WHERE subject_id = ?",
                (subject_id,)
            )
            max_order = cursor.fetchone()[0] or 0

            for verse_id in verse_ids:
                # Get verse data from the verse list widget
                verse_data = self.get_verse_data(verse_id)
                if not verse_data:
                    continue

                # Check if verse already exists
                cursor.execute("""
                    SELECT id FROM subject_verses
                    WHERE subject_id = ? AND verse_reference = ? AND translation = ?
                """, (subject_id, verse_data['reference'], verse_data['translation']))

                if cursor.fetchone():
                    continue  # Skip duplicates

                # Add verse
                max_order += 1
                cursor.execute("""
                    INSERT INTO subject_verses
                    (subject_id, verse_reference, verse_text, translation, order_index)
                    VALUES (?, ?, ?, ?, ?)
                """, (subject_id, verse_data['reference'],
                      verse_data['text'], verse_data['translation'], max_order))

                added_count += 1

            self.db_conn.commit()

            # Reload display if this is the current subject
            if subject_id == self.current_subject_id:
                self.load_subject_verses()

        except Exception as e:
            print(f"⚠️  Error adding verses: {e}")

        return added_count

    def add_verses(self, verse_ids):
        """
        Add verses to current subject.

        Args:
            verse_ids: List of verse IDs to add

        Returns:
            Number of verses added
        """
        # Just delegate to add_verses_to_subject with current subject
        return self.add_verses_to_subject(verse_ids, self.current_subject_id)

    def get_verse_data(self, verse_id):
        """Extract verse data from verse ID."""
        # Determine which window has this verse
        for window_id in ['search', 'reading']:
            verse_list = self.parent_app.verse_lists[window_id]
            if verse_id in verse_list.verse_items:
                item, verse_widget = verse_list.verse_items[verse_id]
                return {
                    'reference': f"{verse_widget.book_abbrev} {verse_widget.chapter}:{verse_widget.verse_number}",
                    'text': verse_widget.text,
                    'translation': verse_widget.translation
                }
        return None

    def load_subject_verses(self):
        """Load verses for current subject."""
        if not self.current_subject_id:
            return

        try:
            cursor = self.db_conn.cursor()

            # Check if subject_comments table exists (new schema) or if comments column exists (old schema)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subject_comments'")
            has_comments_table = cursor.fetchone() is not None

            # Get Bible database connection for book order lookup
            bible_db = self.parent_app.search_controller.bible_search.db_path

            if has_comments_table:
                # New schema: comments in separate table
                cursor.execute("""
                    SELECT sv.id, sv.verse_reference, sv.verse_text, sv.translation, sc.comment as comments,
                           CAST(substr(sv.verse_reference, instr(sv.verse_reference, ' ') + 1,
                                instr(sv.verse_reference || ':', ':') - instr(sv.verse_reference, ' ') - 1) AS INTEGER) as chapter_num,
                           CAST(substr(sv.verse_reference, instr(sv.verse_reference, ':') + 1) AS INTEGER) as verse_num,
                           substr(sv.verse_reference, 1, instr(sv.verse_reference, ' ') - 1) as book_abbr
                    FROM subject_verses sv
                    LEFT JOIN subject_comments sc ON sv.id = sc.verse_id AND sv.subject_id = sc.subject_id
                    WHERE sv.subject_id = ?
                """, (self.current_subject_id,))
            else:
                # Old schema: comments as column in subject_verses
                cursor.execute("""
                    SELECT id, verse_reference, verse_text, translation, comments,
                           CAST(substr(verse_reference, instr(verse_reference, ' ') + 1,
                                instr(verse_reference || ':', ':') - instr(verse_reference, ' ') - 1) AS INTEGER) as chapter_num,
                           CAST(substr(verse_reference, instr(verse_reference, ':') + 1) AS INTEGER) as verse_num,
                           substr(verse_reference, 1, instr(verse_reference, ' ') - 1) as book_abbr
                    FROM subject_verses
                    WHERE subject_id = ?
                """, (self.current_subject_id,))

            verses = cursor.fetchall()

            # Sort verses by biblical order using books table from bibles.db
            import sqlite3
            bible_conn = sqlite3.connect(bible_db)
            bible_conn.row_factory = sqlite3.Row
            bible_cursor = bible_conn.cursor()
            bible_cursor.execute("SELECT abbreviation, order_index FROM books")
            book_order = {row['abbreviation']: row['order_index'] for row in bible_cursor.fetchall()}
            bible_conn.close()

            # Sort verses: book order, then chapter, then verse
            verses = sorted(verses, key=lambda v: (
                book_order.get(v['book_abbr'], 999),  # Book order (999 if not found)
                v['chapter_num'],                       # Chapter number
                v['verse_num']                          # Verse number
            ))

            self.subject_verse_list.clear_verses()

            for verse in verses:
                verse_id = f"subject_{verse['id']}"
                verse_ref = verse['verse_reference']

                # Parse reference
                parts = verse_ref.rsplit(' ', 1)
                book = parts[0]
                chapter_verse = parts[1].split(':')
                chapter = int(chapter_verse[0])
                verse_num = int(chapter_verse[1])

                self.subject_verse_list.add_verse(
                    verse_id, verse['translation'], book,
                    chapter, verse_num, verse['verse_text']
                )

            # Apply font settings to all loaded verses
            from PyQt6.QtGui import QFont
            verse_size = self.parent_app.verse_font_sizes[self.parent_app.verse_font_size]

            for verse_id, verse_item in self.subject_verse_list.verse_items.items():
                _, verse_widget = verse_item
                verse_font = QFont("IBM Plex Mono")
                verse_font.setBold(False)
                verse_font.setPointSizeF(verse_size)
                verse_widget.text_label.setFont(verse_font)

            # Update size hints after font changes
            self.subject_verse_list.update_item_sizes()

            print(f"✓ Loaded {len(verses)} verse(s) for subject")

        except Exception as e:
            print(f"⚠️  Error loading subject verses: {e}")

    def on_delete_verses(self):
        """Delete selected verses from subject."""
        selected_verse_ids = self.subject_verse_list.get_selected_verses()

        if not selected_verse_ids:
            self.parent_app.message_label.setText("⚠️  No verses selected to delete")
            return

        try:
            cursor = self.db_conn.cursor()

            for verse_id in selected_verse_ids:
                if verse_id.startswith("subject_"):
                    db_id = int(verse_id.split("_")[1])
                    cursor.execute("DELETE FROM subject_verses WHERE id = ?", (db_id,))

            self.db_conn.commit()

            self.load_subject_verses()
            self.parent_app.message_label.setText(
                f"✓ Deleted {len(selected_verse_ids)} verse(s)"
            )

        except Exception as e:
            self.parent_app.message_label.setText(f"⚠️  Error deleting verses: {e}")

    def on_rename_subject(self):
        """Rename the current subject."""
        if not self.current_subject:
            return

        new_name, ok = QInputDialog.getText(
            None,
            "Rename Subject",
            f"Enter new name for subject '{self.current_subject}':",
            text=self.current_subject
        )

        if ok and new_name.strip():
            new_name = new_name.strip()

            try:
                cursor = self.db_conn.cursor()
                cursor.execute("""
                    UPDATE subjects
                    SET name = ?, modified_date = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (new_name, self.current_subject_id))
                self.db_conn.commit()

                self.current_subject = new_name
                self.load_subjects()
                self.subject_dropdown.setCurrentText(new_name)

                self.parent_app.message_label.setText(f"✓ Renamed to: {new_name}")

            except sqlite3.IntegrityError:
                self.parent_app.message_label.setText(f"⚠️  Subject '{new_name}' already exists")
            except Exception as e:
                self.parent_app.message_label.setText(f"⚠️  Error renaming: {e}")

    def on_delete_subject(self):
        """Delete the entire subject and all its verses."""
        if not self.current_subject:
            return

        # Count verses and comments
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM subject_verses WHERE subject_id = ?",
                (self.current_subject_id,)
            )
            verse_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM subject_verses
                WHERE subject_id = ? AND comments != ''
            """, (self.current_subject_id,))
            comment_count = cursor.fetchone()[0]

            # Build warning message
            msg = f"Delete subject '{self.current_subject}'?\n\n"
            msg += f"This will permanently delete:\n"
            msg += f"  • The subject '{self.current_subject}'\n"
            msg += f"  • All {verse_count} verse(s) in this subject\n"
            if comment_count > 0:
                msg += f"  • All {comment_count} comment(s) associated with these verses\n"

            reply = QMessageBox.question(
                None, "Delete Subject",
                msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                cursor.execute("DELETE FROM subjects WHERE id = ?", (self.current_subject_id,))
                self.db_conn.commit()

                self.current_subject = None
                self.current_subject_id = None
                self.subject_verse_list.clear_verses()
                self.load_subjects()

                self.parent_app.message_label.setText("✓ Subject deleted")

        except Exception as e:
            self.parent_app.message_label.setText(f"⚠️  Error deleting subject: {e}")

    def on_clear_subject(self):
        """Clear subject display without deleting data."""
        self.current_subject = None
        self.current_subject_id = None
        self.subject_verse_list.clear_verses()
        self.subject_dropdown.setCurrentIndex(0)
        self.update_button_states()
        self.parent_app.message_label.setText("✓ Subject cleared from display")

    def on_subject_verse_clicked(self, verse_id):
        """Handle verse click in Window 4."""
        # Activate subject window
        self.parent_app.set_active_window('subject')
        print(f"Subject verse clicked: {verse_id}")

        # Load comment for this verse in Window 5
        if verse_id.startswith("subject_"):
            db_id = int(verse_id.split("_")[1])
            # Get reference to comment manager through subject manager
            if (self.parent_app.subject_manager and
                self.parent_app.subject_manager.comment_manager):
                self.parent_app.subject_manager.comment_manager.load_comment_for_verse(db_id)
                print(f"✓ Loaded comment for verse ID: {db_id}")

    def on_subject_selection_changed(self):
        """Handle selection changes in Window 4."""
        self.update_button_states()

    def update_button_states(self):
        """Update button enabled/disabled states."""
        has_subject = self.current_subject_id is not None
        has_checked = self.subject_verse_list.get_selected_count() > 0

        # Acquire button state is managed by parent_app.update_subject_acquire_button()
        # which considers both subject selection AND verse selections in Windows 2/3
        # So we only update it here if there are no selections in Windows 2/3
        if self.parent_app:
            search_selections = self.parent_app.verse_lists['search'].get_selected_count()
            reading_selections = self.parent_app.verse_lists['reading'].get_selected_count()
            if search_selections == 0 and reading_selections == 0:
                # No selections in Windows 2/3, disable Acquire if no subject
                self.acquire_btn.setEnabled(has_subject)

        self.delete_btn.setEnabled(has_checked)
        self.rename_btn.setEnabled(has_subject)
        self.delete_subject_btn.setEnabled(has_subject)
        self.clear_subject_btn.setEnabled(has_subject)

    def get_selected_verse_ids(self):
        """
        Get database IDs of selected (checked) verses.

        Returns:
            List of verse IDs from database
        """
        selected_verse_ids = []

        if not self.current_subject_id:
            return selected_verse_ids

        # Get checked verse references
        checked_refs = self.subject_verse_list.get_selected_verses()

        # Map references to database IDs
        for verse_ref in checked_refs:
            if verse_ref in self.subject_verse_list.verse_items:
                # Get the verse widget
                _, widget = self.subject_verse_list.verse_items[verse_ref]

                # Parse reference to get database ID
                # verse_ref format: "book chapter:verse (translation)"
                try:
                    cursor = self.db_conn.cursor()
                    cursor.execute("""
                        SELECT id FROM subject_verses
                        WHERE subject_id = ?
                        ORDER BY id
                    """, (self.current_subject_id,))

                    rows = cursor.fetchall()
                    for row in rows:
                        selected_verse_ids.append(row[0])

                except Exception as e:
                    print(f"Error getting verse ID: {e}")

        return selected_verse_ids

    def cleanup(self):
        """Clean up resources."""
        pass
