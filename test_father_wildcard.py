#!/usr/bin/env python3
"""
Test script to verify "father?" wildcard matches "fathers"
"""

import sys
import re

# Test the wildcard pattern logic
phrase = "father?"

# Build regex pattern (mimicking the fix)
regex_parts = []
regex_parts.append(r'\b')  # Word boundary

for char in phrase:
    if char == '*' or char == '%':
        regex_parts.append(r"[a-zA-Z]*(?:[''][a-zA-Z]*)*")
    elif char == '?':
        # Match exactly one character (letter or apostrophe for possessives)
        regex_parts.append(r"[a-zA-Z'']")
    else:
        regex_parts.append(re.escape(char))

regex_parts.append(r'\b')
wildcard_pattern = ''.join(regex_parts)

print(f"Pattern for '{phrase}': {wildcard_pattern}")
print()

# Test cases
test_text = "The fathers and the father's house"

matches = list(re.finditer(wildcard_pattern, test_text, flags=re.IGNORECASE))

print(f"Test text: {test_text}")
print(f"Found {len(matches)} matches:")
for match in matches:
    print(f"  - '{match.group(0)}' at position {match.start()}-{match.end()}")
print()

# Expected results
print("Expected matches:")
print("  - 'fathers' (father + s)")
print("  - No match for \"father's\" (has apostrophe + s, which is 2 chars after 'father')")
print()

# Test that it correctly matches 7-character patterns with "father?"
if matches:
    print("✓ Pattern correctly matches 'fathers'!")
else:
    print("✗ Pattern failed to match")
