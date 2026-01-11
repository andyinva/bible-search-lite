"""
Custom PyQt6 widgets for Bible Search application.

This module contains reusable UI components for displaying and managing Bible verses:
- VerseItemWidget: Individual verse display with checkbox selection
- VerseListWidget: Scrollable container for multiple verses
- SectionWidget: Titled frame container for organizing UI sections

Author: Andrew Hopkins
"""

from PyQt6.QtWidgets import (QWidget, QLabel, QCheckBox, QVBoxLayout,
                             QHBoxLayout, QScrollArea, QFrame, QSizePolicy,
                             QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont


class VerseItemWidget(QWidget):
    """
    Individual verse display with checkbox and formatted text.
    
    Displays a single Bible verse in a consistent format with:
    - Checkbox for selection
    - Translation abbreviation (e.g., KJV, NIV)
    - Book abbreviation (e.g., Gen, Mat)
    - Chapter and verse numbers
    - Full verse text with word wrapping
    
    Signals:
        selection_changed(str, bool): Emitted when checkbox state changes
            Args:
                verse_id (str): Unique identifier for this verse
                is_selected (bool): New selection state
                
        verse_clicked(str): Emitted when verse is clicked for navigation
            Args:
                verse_id (str): Unique identifier for this verse
    
    Example:
        >>> verse = VerseItemWidget(
        ...     verse_id="search_1",
        ...     translation="KJV",
        ...     book_abbrev="Gen",
        ...     chapter=1,
        ...     verse_number=1,
        ...     text="In the beginning God created the heaven and the earth."
        ... )
        >>> verse.selection_changed.connect(on_selection_changed)
    """
    
    selection_changed = pyqtSignal(str, bool)  # verse_id, is_selected
    verse_clicked = pyqtSignal(str)  # verse_id for navigation
    
    def __init__(self, verse_id, translation, book_abbrev, chapter, verse_number, 
                 text, window_id=None, parent=None):
        """
        Initialize a verse display widget.
        
        Args:
            verse_id (str): Unique identifier for this verse
            translation (str): Bible translation abbreviation (e.g., "KJV")
            book_abbrev (str): Book abbreviation (e.g., "Gen", "Mat")
            chapter (int): Chapter number
            verse_number (int): Verse number within the chapter
            text (str): Full verse text to display
            window_id (str, optional): ID of the parent window (e.g., "search", "reading")
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        self.verse_id = verse_id
        self.translation = translation
        self.book_abbrev = book_abbrev
        self.chapter = chapter
        self.verse_number = verse_number
        self.text = text
        self.window_id = window_id  # Store which window this verse belongs to
        self.is_highlighted = False  # Track if this verse is highlighted for navigation

        self.setup_ui()
        self.setup_styling()
        
    def setup_ui(self):
        """
        Create the widget layout with checkbox, reference, and text.
        
        Layout structure:
        - Checkbox (20px fixed width)
        - Reference label (110px fixed width)
        - Verse text (expandable with word wrap)
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(3, 1, 3, 1)  # Compact margins
        layout.setSpacing(5)  # Minimal spacing between checkbox and text
        
        # Checkbox (fixed width for alignment) - very small with checkmark
        self.checkbox = QCheckBox()
        self.checkbox.setFixedWidth(16)  # Even smaller
        # Very small checkbox - simple color fill when checked (most reliable)
        self.checkbox.setStyleSheet("""
            QCheckBox {
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 11px;
                height: 11px;
                border: 1px solid #999;
                border-radius: 2px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #333;
                background-color: #333;
            }
        """)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        layout.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignTop)

        # Combined reference and text as a single label with word wrap
        ref_text = f"{self.translation} {self.book_abbrev} {self.chapter}:{self.verse_number}"
        combined_text = f"{ref_text} - {self.text}"
        self.text_label = QLabel(combined_text)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        # Remove minimum height to allow compact display
        layout.addWidget(self.text_label, stretch=1)

        # Keep reference_label as attribute for compatibility (points to same label)
        self.reference_label = self.text_label
        self.reference_text = ref_text
        
        # Make the entire widget clickable for navigation
        self.mousePressEvent = self.on_verse_clicked

        # Set height for proper scrolling - compact
        self.setMinimumHeight(22)  # Compact but readable

    def setup_styling(self):
        """
        Apply styling to the verse item.
        
        Styles include:
        - White background with gray bottom border
        - Hover effect (light gray background)
        - Font sizes and colors for reference and text
        """
        self.setStyleSheet("""
            VerseItemWidget {
                background-color: white;
                border: none;
                padding: 1px;
                margin: 0px;
            }
            VerseItemWidget:hover {
                background-color: #f5f5f5;
            }
            QLabel {
                background-color: transparent;
                color: #333;
                padding: 0px;
                margin: 0px;
                line-height: 1.4;
            }
        """)
        
        # Style the combined text label
        font = QFont("IBM Plex Mono")
        font.setBold(False)

        # Try to get font size from main window, default to 9 if not found
        font_size = 9.0
        current = self.parent()
        while current and font_size == 9.0:
            if hasattr(current, 'main_window') and current.main_window:
                if hasattr(current.main_window, 'verse_font_sizes') and hasattr(current.main_window, 'verse_font_size'):
                    font_size = current.main_window.verse_font_sizes[current.main_window.verse_font_size]
                    break
            current = current.parent() if hasattr(current, 'parent') else None

        font.setPointSizeF(font_size)
        self.text_label.setFont(font)

        # Add line-height for consistent wrapped text spacing
        self.text_label.setStyleSheet("""
            QLabel {
                color: black;
                line-height: 13px;
                padding: 0px;
            }
        """)

    def sizeHint(self):
        """Return recommended size for this widget - very compact"""
        from PyQt6.QtCore import QSize
        # Very compact: minimal spacing
        # Assuming ~75 chars per line at 9pt font, ~15px per line
        text_lines = max(1, len(self.text) // 75)
        height = 18 + (text_lines * 15)  # Very compact base + text height
        return QSize(600, min(height, 120))  # Cap at 120px per verse

    def minimumSizeHint(self):
        """Return minimum size for this widget - very compact"""
        from PyQt6.QtCore import QSize
        return QSize(200, 18)  # Very compact minimal height

    def apply_current_style(self):
        """
        Apply the appropriate style based on current state (highlighted, checked, or normal).

        Priority order:
        1. Gray highlight (if is_highlighted is True)
        2. Blue selection (if checkbox is checked)
        3. Normal white background
        """
        if self.is_highlighted:
            # Gray highlight for navigation
            self.setStyleSheet("""
                VerseItemWidget {
                    background-color: #e0e0e0;
                    border-bottom: 1px solid #b0b0b0;
                    border-left: 3px solid #808080;
                    padding: 2px;
                }
            """)
        elif self.checkbox.isChecked():
            # Blue selection for checked verses
            self.setStyleSheet("""
                VerseItemWidget {
                    background-color: #e6f3ff;
                    border-bottom: 1px solid #b3d9ff;
                    border-left: 3px solid #0078d4;
                    padding: 2px;
                }
            """)
        else:
            # Normal white background
            self.setup_styling()

    def on_checkbox_changed(self, state):
        """
        Handle checkbox state change and emit selection_changed signal.

        Args:
            state (int): Qt.CheckState value (Checked or Unchecked)

        Side Effects:
            - Emits selection_changed signal
            - Updates visual styling to show selection
        """
        is_selected = state == Qt.CheckState.Checked.value
        self.selection_changed.emit(self.verse_id, is_selected)

        # Update visual feedback based on all states
        self.apply_current_style()
            
    def on_verse_clicked(self, event):
        """
        Handle verse click for navigation and selection.

        Args:
            event (QMouseEvent): Mouse press event

        Side Effects:
            - Activates the parent window
            - Emits verse_clicked signal for navigation
        """
        # First, try to activate this window by finding the VerseListWidget parent
        # Climb up the widget tree until we find a widget with 'window_id' attribute
        current = self.parent()
        depth = 0
        max_depth = 10  # Safety limit
        main_window_ref = None

        while current and depth < max_depth:
            depth += 1
            if hasattr(current, 'window_id') and hasattr(current, 'main_window'):
                # Found the VerseListWidget!
                main_window_ref = current.main_window
                window_id = current.window_id

                # Block verse navigation if selection is locked
                if main_window_ref and main_window_ref.selection_locked:
                    print(f"🔒 Navigation blocked - selection is locked")
                    return  # Don't navigate, don't emit signal

                print(f"🖱️  Verse clicked in '{window_id}' → Activating window (depth: {depth})")
                main_window_ref.set_active_window(window_id)
                current.setFocus()  # Also set focus for Ctrl+A
                break
            current = current.parent()

        if depth >= max_depth:
            print(f"⚠️  Could not find VerseListWidget parent for {self.verse_id}")

        # Then emit the navigation signal
        self.verse_clicked.emit(self.verse_id)
        
    def set_selected(self, selected):
        """
        Set checkbox state programmatically.
        
        Args:
            selected (bool): True to check the checkbox, False to uncheck
        """
        self.checkbox.setChecked(selected)
        
    def is_selected(self):
        """
        Return current selection state.
        
        Returns:
            bool: True if checkbox is checked, False otherwise
        """
        return self.checkbox.isChecked()
        
    def get_verse_reference(self):
        """
        Return formatted verse reference.
        
        Returns:
            str: Formatted reference (e.g., "KJV Gen 1:1")
        """
        return f"{self.translation} {self.book_abbrev} {self.chapter}:{self.verse_number}"
        
    def highlight_search_terms(self, search_terms):
        """
        Highlight search terms in the verse text.
        
        Args:
            search_terms (list): List of terms to highlight
            
        Note:
            In a full implementation, this would use HTML or rich text formatting.
            Currently implements simple text replacement.
        """
        if not search_terms:
            return

        text = self.text
        for term in search_terms:
            # Simple highlighting - in full implementation would use HTML or rich text
            text = text.replace(term, f"<b><u>{term}</u></b>")

        self.text_label.setText(text)

    def set_highlighted(self, highlighted):
        """
        Highlight this verse as the navigation target.

        Args:
            highlighted (bool): True to highlight, False to remove highlighting

        Side Effects:
            - Changes background color and border
            - Provides visual feedback for current navigation position
        """
        from PyQt6.QtGui import QPalette, QColor

        if highlighted:
            # Use palette for more reliable background color - blue tint
            self.setAutoFillBackground(True)
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Window, QColor(214, 233, 255))  # #D6E9FF blue tint
            self.setPalette(palette)

            # Add border styling - blue borders
            self.setStyleSheet("""
                VerseItemWidget {
                    border-bottom: 1px solid #A0C8FF;
                    border-left: 3px solid #4A90E2;
                    padding: 1px;
                    margin: 0px;
                }
            """)
        else:
            self.setAutoFillBackground(False)
            self.setup_styling()


class VerseListWidget(QWidget):
    """
    Container widget for managing multiple verse items using QListWidget.

    Provides a high-performance scrollable list of VerseItemWidget instances with:
    - Automatic selection tracking
    - Batch operations (select all, select none)
    - Active/inactive visual states
    - Scroll-to-verse functionality
    - Optimized scrolling performance with QListWidget

    Signals:
        selection_changed(): Emitted when any verse selection changes
        verse_navigation_requested(str): Emitted when navigation to a verse is requested
            Args:
                verse_id (str): Verse to navigate to

    Example:
        >>> verse_list = VerseListWidget("search")
        >>> verse_list.add_verse("v1", "KJV", "Gen", 1, 1, "In the beginning...")
        >>> verse_list.selection_changed.connect(on_selection_changed)
    """

    selection_changed = pyqtSignal()  # Emitted when selection changes
    verse_navigation_requested = pyqtSignal(str)  # verse_id for navigation

    def __init__(self, window_id, parent=None):
        """
        Initialize the verse list container.

        Args:
            window_id (str): Identifier for this window (e.g., "search", "reading", "subject")
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        self.window_id = window_id
        self.verse_items = {}  # verse_id -> (QListWidgetItem, VerseItemWidget)
        self.selected_verses = set()  # Set of selected verse_ids
        self.currently_highlighted_verse = None  # Track clicked verse for gray highlighting

        self.setup_ui()

        # Enable keyboard focus to receive key events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # CRITICAL: Allow this widget to expand to fill available space
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

    def setup_ui(self):
        """
        Create the list widget layout.

        Structure:
        - Main layout contains QListWidget wrapped in a beveled frame
        - Each list item contains a VerseItemWidget
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create beveled frame for the list
        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.Shape.Panel)
        list_frame.setFrameShadow(QFrame.Shadow.Sunken)
        list_frame.setLineWidth(3)
        list_frame.setMidLineWidth(2)

        frame_layout = QVBoxLayout(list_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)

        # Create QListWidget for optimized scrolling
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(0)  # No spacing for maximum compactness
        self.list_widget.setUniformItemSizes(False)  # Dynamic heights for proper wrapping
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Pass focus to parent

        # Enable smooth pixel-based scrolling
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)

        # CRITICAL: Set size policy to allow expansion
        self.list_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # Install event filter to activate window when clicking anywhere in list
        self.list_widget.viewport().installEventFilter(self)

        # Add list to frame, then frame to main layout
        frame_layout.addWidget(self.list_widget)
        main_layout.addWidget(list_frame)

        # Styling (no border needed since frame provides it)
        self.setStyleSheet("""
            VerseListWidget {
                background-color: white;
            }
            VerseListWidget:focus {
                border: 2px solid #0078d4;
            }
            QListWidget {
                border: none;
                background-color: white;
            }
            QListWidget::item {
                border: none;
                padding: 0px;
                margin: 0px;
            }
        """)

    def add_verse(self, verse_id, translation, book_abbrev, chapter, verse_number, text):
        """
        Add a verse to the list.

        Args:
            verse_id (str): Unique identifier for the verse
            translation (str): Bible translation abbreviation
            book_abbrev (str): Book abbreviation
            chapter (int): Chapter number
            verse_number (int): Verse number
            text (str): Full verse text

        Note:
            If verse_id already exists, the verse is not added again
        """
        if verse_id in self.verse_items:
            return  # Verse already exists

        # Create QListWidgetItem
        item = QListWidgetItem(self.list_widget)
        item.setData(Qt.ItemDataRole.UserRole, verse_id)

        # Create VerseItemWidget
        verse_widget = VerseItemWidget(
            verse_id, translation, book_abbrev, chapter,
            verse_number, text, window_id=self.window_id, parent=None
        )
        verse_widget.selection_changed.connect(self.on_verse_selection_changed)
        verse_widget.verse_clicked.connect(self.on_verse_clicked)

        # Set the widget for this item
        item.setSizeHint(verse_widget.sizeHint())
        self.list_widget.setItemWidget(item, verse_widget)

        # Store both item and widget
        self.verse_items[verse_id] = (item, verse_widget)

        # Apply current font size from main window if available
        if hasattr(self, 'main_window') and self.main_window:
            verse_size = self.main_window.verse_font_sizes[self.main_window.verse_font_size]
            font = QFont("IBM Plex Mono")
            font.setBold(False)
            font.setPointSizeF(verse_size)  # Use setPointSizeF for fractional sizes
            verse_widget.text_label.setFont(font)

    def on_verse_selection_changed(self, verse_id, is_selected):
        """
        Handle individual verse selection change.

        Args:
            verse_id (str): Verse that changed selection
            is_selected (bool): New selection state

        Side Effects:
            - Updates selected_verses set
            - Emits selection_changed signal
            - Makes this window active in main window
        """
        if is_selected:
            self.selected_verses.add(verse_id)
        else:
            self.selected_verses.discard(verse_id)

        self.selection_changed.emit()

        # Make this window active when a checkbox is clicked
        if hasattr(self, 'main_window'):
            self.main_window.set_active_window(self.window_id)
            # Directly call button update to ensure it triggers
            self.main_window.update_acquire_button_state()

            # Lock/unlock selection mode based on whether ANY boxes are checked
            if len(self.selected_verses) > 0:
                # Lock mode (manual selection, not Ctrl+A)
                self.main_window.lock_selection_mode(is_ctrl_a=False)
            else:
                # All unchecked - unlock
                self.main_window.unlock_selection_mode()

    def on_verse_clicked(self, verse_id):
        """
        Handle verse click for navigation.

        Args:
            verse_id (str): Verse that was clicked

        Side Effects:
            - Makes this window active
            - Updates acquire button state
            - Emits verse_navigation_requested signal
        """
        if hasattr(self, 'main_window'):
            # Make this window active when a verse is clicked
            self.main_window.set_active_window(self.window_id)
            # Update button state
            self.main_window.update_acquire_button_state()

        # Emit navigation signal (no checkbox toggling - user must click checkbox directly)
        self.verse_navigation_requested.emit(verse_id)

        # Highlight this verse in gray
        self.set_highlighted_verse(verse_id)

    def set_highlighted_verse(self, verse_id):
        """
        Highlight a verse with gray background when clicked.

        Args:
            verse_id (str): Verse to highlight (or None to clear highlight)
        """
        # Clear ALL previous highlights across ALL windows (including old blue highlights)
        if hasattr(self, 'main_window') and self.main_window:
            # Clear highlights in all verse list windows
            for window_name in ['search', 'reading']:
                if window_name in self.main_window.verse_lists:
                    verse_list = self.main_window.verse_lists[window_name]
                    # Clear the currently_highlighted_verse tracking
                    if verse_list.currently_highlighted_verse and verse_list.currently_highlighted_verse in verse_list.verse_items:
                        item, verse_widget = verse_list.verse_items[verse_list.currently_highlighted_verse]
                        verse_widget.is_highlighted = False
                        verse_widget.apply_current_style()
                        verse_list.currently_highlighted_verse = None

                    # Also clear old-style blue highlighting (from Window 2 clicks)
                    from PyQt6.QtGui import QColor, QBrush
                    for vid, (list_item, vw) in verse_list.verse_items.items():
                        vw.set_highlighted(False)
                        list_item.setBackground(QBrush(QColor(255, 255, 255)))  # White

        # Set new highlight
        self.currently_highlighted_verse = verse_id
        if verse_id and verse_id in self.verse_items:
            item, verse_widget = self.verse_items[verse_id]
            verse_widget.is_highlighted = True
            verse_widget.apply_current_style()

    def clear_verses(self):
        """
        Remove all verses from the list.

        Side Effects:
            - Removes all verse widgets
            - Clears verse_items dictionary
            - Clears selected_verses set
            - Clears highlighted verse
            - Emits selection_changed signal
        """
        self.list_widget.clear()
        self.verse_items.clear()
        self.selected_verses.clear()
        self.currently_highlighted_verse = None
        self.selection_changed.emit()

    def get_selected_verses(self):
        """
        Return list of selected verse IDs.

        Returns:
            list: List of verse_id strings for all selected verses
        """
        return list(self.selected_verses)

    def select_all(self):
        """
        Select all verses in the list.

        Side Effects:
            - Checks all verse checkboxes
            - Updates selection state for all verses
        """
        for item, verse_widget in self.verse_items.values():
            verse_widget.set_selected(True)

    def select_none(self):
        """
        Deselect all verses in the list.

        Side Effects:
            - Unchecks all verse checkboxes
            - Clears selection state for all verses
        """
        for item, verse_widget in self.verse_items.values():
            verse_widget.set_selected(False)

    def update_item_sizes(self):
        """
        Update size hints for all items to reflect current widget sizes.
        Call this after changing spacing/padding to reflow the layout.
        """
        for item, verse_widget in self.verse_items.values():
            item.setSizeHint(verse_widget.sizeHint())
        # Force the list widget to update its layout
        self.list_widget.update()

    def eventFilter(self, obj, event):
        """
        Event filter to catch mouse clicks on the QListWidget viewport.

        This ensures clicking anywhere in the list (not just the sidebar)
        will activate this window.

        Args:
            obj: The object that generated the event
            event: The event to filter

        Returns:
            bool: True if event was handled, False to pass it on
        """
        from PyQt6.QtCore import QEvent

        # Only handle mouse press events on the list viewport
        if obj == self.list_widget.viewport() and event.type() == QEvent.Type.MouseButtonPress:
            # Block window switching if selection is locked
            if hasattr(self, 'main_window') and self.main_window:
                if not self.main_window.selection_locked:
                    # Make this window active when clicked
                    print(f"🖱️  Clicked in list viewport '{self.window_id}' → Activating")
                    self.main_window.set_active_window(self.window_id)
                    self.setFocus()
                else:
                    print(f"🔒 Window switching blocked - selection is locked")

        # Always pass the event through for normal processing
        return False

    def mousePressEvent(self, event):
        """
        Handle mouse press events for the verse list.

        Makes this window active when clicked anywhere in it.

        Args:
            event (QMouseEvent): Mouse press event
        """
        # Block window switching if selection is locked
        if hasattr(self, 'main_window') and self.main_window:
            if self.main_window.selection_locked:
                print(f"🔒 Window switching blocked - selection is locked")
                return  # Don't allow window changes

        # Make this window active when clicked
        if hasattr(self, 'main_window'):
            print(f"🖱️  Clicked in window '{self.window_id}' → Activating")
            self.main_window.set_active_window(self.window_id)
        else:
            print(f"⚠️  Clicked in window '{self.window_id}' but no main_window reference")

        # Set focus to enable Ctrl+A
        self.setFocus()

        # Pass event to parent for normal processing
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        """
        Handle keyboard events for the verse list.

        Supports:
            - Ctrl+A: Select all verses in the list
            - Ctrl+D: Deselect all verses (unlock)

        Args:
            event (QKeyEvent): The keyboard event
        """
        from PyQt6.QtCore import Qt

        # Check for Ctrl+A (select all)
        if event.key() == Qt.Key.Key_A and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.select_all()
            print(f"📋 Ctrl+A: Selected all {len(self.verse_items)} verses in {self.window_id}")

            # Lock selection mode (Ctrl+A = copy-only)
            if hasattr(self, 'main_window') and self.main_window:
                self.main_window.lock_selection_mode(is_ctrl_a=True)

            event.accept()

        # Check for Ctrl+D (deselect all - unlock)
        elif event.key() == Qt.Key.Key_D and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.select_none()
            print(f"📋 Ctrl+D: Deselected all verses in {self.window_id}")

            # Unlock happens automatically via checkbox change handler
            event.accept()

        else:
            # Pass other key events to parent
            super().keyPressEvent(event)

    def get_verse_count(self):
        """
        Return total number of verses.

        Returns:
            int: Total number of verses in the list
        """
        return len(self.verse_items)

    def get_selected_count(self):
        """
        Return number of selected verses.

        Returns:
            int: Number of currently selected verses
        """
        return len(self.selected_verses)

    def set_active(self, is_active):
        """
        Set visual state for active/inactive window.

        Args:
            is_active (bool): True for active state, False for inactive

        Side Effects:
            - Changes border color and background
            - Enables/disables scrolling for search and reading windows
            - Forces visual update
        """
        if is_active:
            # Use direct property setting instead of CSS
            self.setStyleSheet("")  # Clear any existing styles
            self.list_widget.setStyleSheet("""
                QListWidget {
                    border: 3px solid #0078d4;
                    background-color: white;
                }
                QListWidget::item {
                    border: none;
                    padding: 0px;
                    margin: 0px;
                }
                QListWidget::item:selected {
                    background-color: transparent;
                }
            """)
            # Enable scrolling when active
            self.list_widget.verticalScrollBar().setEnabled(True)
        else:
            self.setStyleSheet("")  # Clear any existing styles
            self.list_widget.setStyleSheet("""
                QListWidget {
                    border: 2px solid #ccc;
                    background-color: white;
                }
                QListWidget::item {
                    border: none;
                    padding: 0px;
                    margin: 0px;
                }
                QListWidget::item:selected {
                    background-color: transparent;
                }
            """)
            # Disable scrolling when inactive (only for search and reading windows)
            if self.window_id in ['search', 'reading']:
                self.list_widget.verticalScrollBar().setEnabled(False)

        # Force update
        self.list_widget.update()
        self.update()

    def scroll_to_verse(self, verse_id):
        """
        Scroll to show a specific verse at the top of the list widget.

        Args:
            verse_id (str): Verse to scroll to

        Side Effects:
            - Adjusts scroll position to show the specified verse
        """
        if verse_id in self.verse_items:
            item, verse_widget = self.verse_items[verse_id]
            self.list_widget.scrollToItem(item, QListWidget.ScrollHint.PositionAtTop)


class SectionWidget(QFrame):
    """
    A section container with title and controls.
    
    Provides a consistent styled frame for major UI sections with:
    - Bold title label
    - Optional controls row (buttons, etc.)
    - Content area
    - Optional settings gear icon
    
    Example:
        >>> controls = create_search_controls()  # Your custom widget
        >>> content = VerseListWidget("search")
        >>> section = SectionWidget("2. Search Results", content, controls)
    """

    def __init__(self, title, content_widget, controls_widget=None,
                 show_settings=False, title_buttons=None, main_window=None, parent=None):
        """
        Initialize a section container.

        Args:
            title (str): Section title text (e.g., "2. Search Results")
            content_widget (QWidget): Main content widget for this section
            controls_widget (QWidget, optional): Controls to display above content
            show_settings (bool): If True, displays a settings gear icon
            title_buttons (list, optional): List of QPushButton widgets to add to title bar
            main_window (QMainWindow, optional): Reference to main window for settings callback
            parent (QWidget, optional): Parent widget
        """
        super().__init__(parent)
        # Set frame style to create beveled/raised 3D effect
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setLineWidth(3)  # Thicker border for more pronounced 3D effect
        self.setMidLineWidth(2)  # Additional thickness for deeper bevel
        self.setStyleSheet("""
            SectionWidget {
                background-color: transparent;
                margin: 2px;
            }
        """)

        # Store references for title click handling
        self.content_widget = content_widget
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 0, 3, 3)  # Reduced top margin from 3 to 0
        layout.setSpacing(2)

        # Title row with optional buttons
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        # Title label - make it clickable to activate the window
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 11px;
                color: #333;
                background-color: transparent;
                padding: 0px;
            }
            QLabel:hover {
                color: #0078d4;
            }
        """)

        # Make title clickable to activate window
        if hasattr(content_widget, 'window_id') and main_window:
            def on_title_click(event):
                window_id = content_widget.window_id
                print(f"🖱️  Title clicked: {title} → Activating window '{window_id}'")
                main_window.set_active_window(window_id)
            title_label.mousePressEvent = on_title_click
        else:
            print(f"⚠️  Title '{title}' not clickable: window_id={hasattr(content_widget, 'window_id')}, main_window={main_window is not None}")

        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Add custom title buttons if provided
        if title_buttons:
            for button in title_buttons:
                title_layout.addWidget(button)

        # Settings gear icon (only for message window)
        if show_settings and main_window:
            from PyQt6.QtWidgets import QPushButton
            settings_btn = QPushButton("⚙")
            settings_btn.setFixedSize(24, 24)
            settings_btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #999;
                    border-radius: 3px;
                    font-size: 14px;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border: 1px solid #666;
                }
            """)
            settings_btn.clicked.connect(main_window.show_font_settings)
            title_layout.addWidget(settings_btn)

        layout.addLayout(title_layout)

        # Controls (if provided)
        if controls_widget:
            layout.addWidget(controls_widget)

        # Content area
        layout.addWidget(content_widget)
