#!/usr/bin/env python3
"""
Test highlighting for "father?" pattern
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from bible_search import BibleSearch

# Initialize
bible = BibleSearch()

# Test text
test_text = "The fathers came to meet their father in the house"

# Test query
query = '("sleep*" OR "slep*") AND "father?"'

# Apply highlighting
highlighted = bible.highlight_search_terms(test_text, query)

print(f"Original text: {test_text}")
print(f"Query: {query}")
print(f"Highlighted: {highlighted}")
print()

# Check if "fathers" and "father" are highlighted
if '[father' in highlighted.lower():
    print("✓ 'father' terms are highlighted!")
    if '{s}' in highlighted.lower():
        print("✓ Two-color highlighting detected (green + blue)")
    else:
        print("⚠ Single-color highlighting only")
else:
    print("✗ 'father' terms NOT highlighted")
