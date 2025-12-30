#!/usr/bin/env python3
"""
User Data Service
Handles all database operations for groups, subjects, verses, and comments.
"""

import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import os


class UserDataService:
    """
    Service class for managing user data (groups, subjects, verses, comments).
    Provides CRUD operations with proper error handling and transaction management.
    """
    
    def __init__(self, database_path: str = "user_data.db"):
        """
        Initialize the UserDataService.
        
        Args:
            database_path: Path to the SQLite database file
        """
        self.database_path = database_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Check if database file exists, raise error if not."""
        if not os.path.exists(self.database_path):
            raise FileNotFoundError(
                f"Database file not found: {self.database_path}\n"
                f"Please ensure user_data.db exists in the project directory."
            )
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection.
        
        Returns:
            SQLite connection object
        """
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    # ========================================================================
    # GROUP OPERATIONS
    # ========================================================================
    
    def get_all_groups(self) -> List[Dict]:
        """
        Get all groups ordered by sort_order.
        
        Returns:
            List of group dictionaries with keys: group_id, group_name, 
            description, created_date, sort_order
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT group_id, group_name, description, created_date, sort_order
                FROM groups
                ORDER BY sort_order, group_name
            """)
            
            groups = []
            for row in cursor.fetchall():
                groups.append({
                    'group_id': row['group_id'],
                    'group_name': row['group_name'],
                    'description': row['description'],
                    'created_date': row['created_date'],
                    'sort_order': row['sort_order']
                })
            
            conn.close()
            return groups
            
        except sqlite3.Error as e:
            print(f"Error getting all groups: {e}")
            return []
    
    def get_group_by_id(self, group_id: int) -> Optional[Dict]:
        """
        Get a single group by ID.
        
        Args:
            group_id: The group ID to fetch
            
        Returns:
            Group dictionary or None if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT group_id, group_name, description, created_date, sort_order
                FROM groups
                WHERE group_id = ?
            """, (group_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'group_id': row['group_id'],
                    'group_name': row['group_name'],
                    'description': row['description'],
                    'created_date': row['created_date'],
                    'sort_order': row['sort_order']
                }
            return None
            
        except sqlite3.Error as e:
            print(f"Error getting group {group_id}: {e}")
            return None
    
    def create_group(self, group_name: str, description: str = "", 
                    sort_order: Optional[int] = None) -> Optional[int]:
        """
        Create a new group.
        
        Args:
            group_name: Name of the group (required)
            description: Optional description
            sort_order: Optional sort order (auto-calculated if not provided)
            
        Returns:
            The new group_id or None if creation failed
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Auto-calculate sort_order if not provided
            if sort_order is None:
                cursor.execute("SELECT COALESCE(MAX(sort_order), 0) + 1 FROM groups")
                sort_order = cursor.fetchone()[0]
            
            # Create timestamp
            created_date = datetime.now().isoformat()
            
            # Insert group
            cursor.execute("""
                INSERT INTO groups (group_name, description, created_date, sort_order)
                VALUES (?, ?, ?, ?)
            """, (group_name, description, created_date, sort_order))
            
            group_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Created group '{group_name}' with ID {group_id}")
            return group_id
            
        except sqlite3.Error as e:
            print(f"Error creating group '{group_name}': {e}")
            if conn:
                conn.rollback()
                conn.close()
            return None
    
    def delete_group(self, group_id: int, cascade: bool = False) -> bool:
        """
        Delete a group.
        
        Args:
            group_id: The group ID to delete
            cascade: If True, also delete all subjects in the group.
                    If False, only delete if group has no subjects.
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if group has subjects
            cursor.execute("""
                SELECT COUNT(*) FROM subjects WHERE group_id = ?
            """, (group_id,))
            subject_count = cursor.fetchone()[0]
            
            if subject_count > 0 and not cascade:
                print(f"Cannot delete group {group_id}: has {subject_count} subjects")
                conn.close()
                return False
            
            # If cascade, delete all subjects in the group first
            if cascade and subject_count > 0:
                cursor.execute("""
                    SELECT subject_id FROM subjects WHERE group_id = ?
                """, (group_id,))
                subject_ids = [row[0] for row in cursor.fetchall()]
                
                for subject_id in subject_ids:
                    # Delete subject (this will cascade to verses and comments)
                    self.delete_subject(subject_id)
            
            # Delete the group
            cursor.execute("DELETE FROM groups WHERE group_id = ?", (group_id,))
            
            conn.commit()
            conn.close()
            
            print(f"Deleted group ID {group_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error deleting group {group_id}: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False
    
    # ========================================================================
    # SUBJECT OPERATIONS
    # ========================================================================
    
    def get_subjects_by_group(self, group_id: int) -> List[Dict]:
        """
        Get all subjects for a specific group.
        
        Args:
            group_id: The group ID to fetch subjects for
            
        Returns:
            List of subject dictionaries
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT subject_id, group_id, subject_name, description, 
                       created_date, sort_order
                FROM subjects
                WHERE group_id = ?
                ORDER BY sort_order, subject_name
            """, (group_id,))
            
            subjects = []
            for row in cursor.fetchall():
                subjects.append({
                    'subject_id': row['subject_id'],
                    'group_id': row['group_id'],
                    'subject_name': row['subject_name'],
                    'description': row['description'],
                    'created_date': row['created_date'],
                    'sort_order': row['sort_order']
                })
            
            conn.close()
            return subjects
            
        except sqlite3.Error as e:
            print(f"Error getting subjects for group {group_id}: {e}")
            return []
    
    def get_subject_by_id(self, subject_id: int) -> Optional[Dict]:
        """
        Get a single subject by ID.
        
        Args:
            subject_id: The subject ID to fetch
            
        Returns:
            Subject dictionary or None if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT subject_id, group_id, subject_name, description,
                       created_date, sort_order
                FROM subjects
                WHERE subject_id = ?
            """, (subject_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'subject_id': row['subject_id'],
                    'group_id': row['group_id'],
                    'subject_name': row['subject_name'],
                    'description': row['description'],
                    'created_date': row['created_date'],
                    'sort_order': row['sort_order']
                }
            return None
            
        except sqlite3.Error as e:
            print(f"Error getting subject {subject_id}: {e}")
            return None
    
    def create_subject(self, group_id: int, subject_name: str, 
                      description: str = "", 
                      sort_order: Optional[int] = None) -> Optional[int]:
        """
        Create a new subject.
        
        Args:
            group_id: The group this subject belongs to (required)
            subject_name: Name of the subject (required)
            description: Optional description
            sort_order: Optional sort order (auto-calculated if not provided)
            
        Returns:
            The new subject_id or None if creation failed
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Auto-calculate sort_order if not provided
            if sort_order is None:
                cursor.execute("""
                    SELECT COALESCE(MAX(sort_order), 0) + 1 
                    FROM subjects 
                    WHERE group_id = ?
                """, (group_id,))
                sort_order = cursor.fetchone()[0]
            
            # Create timestamp
            created_date = datetime.now().isoformat()
            
            # Insert subject
            cursor.execute("""
                INSERT INTO subjects (group_id, subject_name, description, 
                                     created_date, sort_order)
                VALUES (?, ?, ?, ?, ?)
            """, (group_id, subject_name, description, created_date, sort_order))
            
            subject_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Created subject '{subject_name}' with ID {subject_id}")
            return subject_id
            
        except sqlite3.Error as e:
            print(f"Error creating subject '{subject_name}': {e}")
            if conn:
                conn.rollback()
                conn.close()
            return None
    
    def delete_subject(self, subject_id: int) -> bool:
        """
        Delete a subject and all its verses and comments.
        
        Args:
            subject_id: The subject ID to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get all verse IDs for this subject (for deleting comments)
            cursor.execute("""
                SELECT id FROM subject_verses WHERE subject_id = ?
            """, (subject_id,))
            verse_ids = [row[0] for row in cursor.fetchall()]
            
            # Delete comments for all verses
            for verse_id in verse_ids:
                cursor.execute("""
                    DELETE FROM verse_comments WHERE subject_verse_id = ?
                """, (verse_id,))
            
            # Delete all verses for this subject
            cursor.execute("""
                DELETE FROM subject_verses WHERE subject_id = ?
            """, (subject_id,))
            
            # Delete the subject itself
            cursor.execute("""
                DELETE FROM subjects WHERE subject_id = ?
            """, (subject_id,))
            
            conn.commit()
            conn.close()
            
            print(f"Deleted subject ID {subject_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error deleting subject {subject_id}: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False
    
    # ========================================================================
    # SUBJECT VERSE OPERATIONS
    # ========================================================================
    
    def get_verses_by_subject(self, subject_id: int) -> List[Dict]:
        """
        Get all verses for a specific subject.
        
        Args:
            subject_id: The subject ID to fetch verses for
            
        Returns:
            List of verse dictionaries with keys: id, subject_id, 
            verse_reference, translation, verse_text, created_timestamp, sort_order
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, subject_id, verse_reference, translation, 
                       verse_text, created_timestamp, sort_order
                FROM subject_verses
                WHERE subject_id = ?
                ORDER BY sort_order
            """, (subject_id,))
            
            verses = []
            for row in cursor.fetchall():
                verses.append({
                    'id': row['id'],  # This is subject_verse_id
                    'subject_id': row['subject_id'],
                    'verse_reference': row['verse_reference'],
                    'translation': row['translation'],
                    'verse_text': row['verse_text'],
                    'created_timestamp': row['created_timestamp'],
                    'sort_order': row['sort_order']
                })
            
            conn.close()
            return verses
            
        except sqlite3.Error as e:
            print(f"Error getting verses for subject {subject_id}: {e}")
            return []
    
    def add_verse_to_subject(self, subject_id: int, verse_reference: str,
                            translation: str, verse_text: str,
                            sort_order: Optional[int] = None) -> Optional[int]:
        """
        Add a verse to a subject.
        
        Args:
            subject_id: The subject to add the verse to
            verse_reference: Bible reference (e.g., "Gen 1:1")
            translation: Translation abbreviation (e.g., "KJV")
            verse_text: The actual verse text
            sort_order: Optional sort order (auto-calculated if not provided)
            
        Returns:
            The new verse ID or None if creation failed
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check for duplicate
            cursor.execute("""
                SELECT id FROM subject_verses
                WHERE subject_id = ? AND verse_reference = ? AND translation = ?
            """, (subject_id, verse_reference, translation))
            
            if cursor.fetchone():
                print(f"Verse {verse_reference} ({translation}) already exists in subject {subject_id}")
                conn.close()
                return None
            
            # Auto-calculate sort_order if not provided
            if sort_order is None:
                cursor.execute("""
                    SELECT COALESCE(MAX(sort_order), 0) + 1 
                    FROM subject_verses 
                    WHERE subject_id = ?
                """, (subject_id,))
                sort_order = cursor.fetchone()[0]
            
            # Create timestamp
            created_timestamp = datetime.now().isoformat()
            
            # Insert verse
            cursor.execute("""
                INSERT INTO subject_verses 
                (subject_id, verse_reference, translation, verse_text, 
                 created_timestamp, sort_order)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (subject_id, verse_reference, translation, verse_text,
                  created_timestamp, sort_order))
            
            verse_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Added verse {verse_reference} to subject {subject_id}")
            return verse_id
            
        except sqlite3.Error as e:
            print(f"Error adding verse to subject: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return None
    
    def delete_verse_from_subject(self, verse_id: int) -> bool:
        """
        Delete a verse from a subject (and its comment if any).
        
        Args:
            verse_id: The subject_verse ID to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Delete comment if it exists
            cursor.execute("""
                DELETE FROM verse_comments WHERE subject_verse_id = ?
            """, (verse_id,))
            
            # Delete the verse
            cursor.execute("""
                DELETE FROM subject_verses WHERE id = ?
            """, (verse_id,))
            
            conn.commit()
            conn.close()
            
            print(f"Deleted verse ID {verse_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error deleting verse {verse_id}: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False
    
    def find_subjects_containing_verse(self, verse_reference: str, 
                                      translation: str) -> List[Dict]:
        """
        Find all subjects that contain a specific verse.
        
        Args:
            verse_reference: Bible reference (e.g., "Gen 1:1")
            translation: Translation abbreviation (e.g., "KJV")
            
        Returns:
            List of subject dictionaries containing this verse
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT s.subject_id, s.group_id, s.subject_name, 
                               s.description, s.created_date, s.sort_order
                FROM subjects s
                JOIN subject_verses sv ON s.subject_id = sv.subject_id
                WHERE sv.verse_reference = ? AND sv.translation = ?
                ORDER BY s.sort_order, s.subject_name
            """, (verse_reference, translation))
            
            subjects = []
            for row in cursor.fetchall():
                subjects.append({
                    'subject_id': row['subject_id'],
                    'group_id': row['group_id'],
                    'subject_name': row['subject_name'],
                    'description': row['description'],
                    'created_date': row['created_date'],
                    'sort_order': row['sort_order']
                })
            
            conn.close()
            return subjects
            
        except sqlite3.Error as e:
            print(f"Error finding subjects for verse {verse_reference}: {e}")
            return []
    
    # ========================================================================
    # COMMENT OPERATIONS
    # ========================================================================
    
    def get_comment_for_verse(self, subject_verse_id: int) -> Optional[Dict]:
        """
        Get the comment for a specific verse in a subject.
        
        Args:
            subject_verse_id: The subject_verse ID
            
        Returns:
            Comment dictionary or None if no comment exists
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT comment_id, subject_verse_id, comment_text,
                       created_date, modified_date
                FROM verse_comments
                WHERE subject_verse_id = ?
            """, (subject_verse_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'comment_id': row['comment_id'],
                    'subject_verse_id': row['subject_verse_id'],
                    'comment_text': row['comment_text'],
                    'created_date': row['created_date'],
                    'modified_date': row['modified_date']
                }
            return None
            
        except sqlite3.Error as e:
            print(f"Error getting comment for verse {subject_verse_id}: {e}")
            return None
    
    def save_comment(self, subject_verse_id: int, comment_text: str) -> Optional[int]:
        """
        Save or update a comment for a verse.
        
        Args:
            subject_verse_id: The subject_verse ID
            comment_text: The comment text
            
        Returns:
            The comment_id or None if save failed
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if comment already exists
            cursor.execute("""
                SELECT comment_id FROM verse_comments
                WHERE subject_verse_id = ?
            """, (subject_verse_id,))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing comment
                comment_id = existing[0]
                modified_date = datetime.now().isoformat()
                
                cursor.execute("""
                    UPDATE verse_comments
                    SET comment_text = ?, modified_date = ?
                    WHERE comment_id = ?
                """, (comment_text, modified_date, comment_id))
                
                print(f"Updated comment {comment_id}")
            else:
                # Create new comment
                created_date = datetime.now().isoformat()
                
                cursor.execute("""
                    INSERT INTO verse_comments
                    (subject_verse_id, comment_text, created_date, modified_date)
                    VALUES (?, ?, ?, ?)
                """, (subject_verse_id, comment_text, created_date, created_date))
                
                comment_id = cursor.lastrowid
                print(f"Created comment {comment_id}")
            
            conn.commit()
            conn.close()
            
            return comment_id
            
        except sqlite3.Error as e:
            print(f"Error saving comment: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return None
    
    def delete_comment(self, comment_id: int) -> bool:
        """
        Delete a comment.
        
        Args:
            comment_id: The comment ID to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM verse_comments WHERE comment_id = ?
            """, (comment_id,))
            
            conn.commit()
            conn.close()
            
            print(f"Deleted comment ID {comment_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"Error deleting comment {comment_id}: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False
