#!/usr/bin/env python3
"""Test filter with word placeholder (&)"""

from bible_search import BibleSearch
import re

def extract_phrase_patterns(results, query):
    """Simulate the _extract_phrase_patterns method"""
    phrase_counts = {}

    # Build regex pattern
    regex_parts = []
    parts = query.split()

    for part in parts:
        if part == '&':
            regex_parts.append(r'(\w+)')
        else:
            word_pattern = part.replace('*', r'\w*').replace('?', r'\w')
            regex_parts.append(f'({word_pattern})')

    regex_pattern = r'\b' + r'\s+'.join(regex_parts) + r'\b'

    # Extract phrases
    for result in results:
        text = result.text.replace('[', '').replace(']', '')
        for match in re.finditer(regex_pattern, text, flags=re.IGNORECASE):
            matched_words = match.groups()
            phrase = ' '.join(word.capitalize() for word in matched_words)
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

    return phrase_counts

# Initialize
bible = BibleSearch('database/bibles.db')

print("=" * 70)
print("Test 1: who & sen*")
print("=" * 70)

results = bible.search_verses(
    query='who & sen*',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search results: {len(results)} verses")
print()

phrases = extract_phrase_patterns(results, 'who & sen*')
print("Filter would show:")
print(f"  Found {len(phrases)} phrase variation(s) in {len(results)} verse(s)")
print()
for phrase, count in sorted(phrases.items(), key=lambda x: (-x[1], x[0])):
    print(f"  ☑ {phrase} ({count})")

print()
print("=" * 70)
print("Test 2: I & you (first 50 results)")
print("=" * 70)

results2 = bible.search_verses(
    query='I & you',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search results: {len(results2)} verses (analyzing first 50)")
print()

phrases2 = extract_phrase_patterns(results2[:50], 'I & you')
print("Filter would show (top 10):")
print(f"  Found {len(phrases2)} phrase variation(s)")
print()
for phrase, count in sorted(phrases2.items(), key=lambda x: (-x[1], x[0]))[:10]:
    print(f"  ☑ {phrase} ({count})")

print()
print("=" * 70)
print("Test 3: love & & God (two placeholders)")
print("=" * 70)

results3 = bible.search_verses(
    query='love & & God',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search results: {len(results3)} verses")
print()

if results3:
    phrases3 = extract_phrase_patterns(results3, 'love & & God')
    print("Filter would show:")
    print(f"  Found {len(phrases3)} phrase variation(s)")
    print()
    for phrase, count in sorted(phrases3.items(), key=lambda x: (-x[1], x[0]))[:10]:
        print(f"  ☑ {phrase} ({count})")
else:
    print("  No results found")

print()
print("✅ All tests completed!")
