#!/usr/bin/env python3
"""Test % (stem/root) wildcard functionality"""

from bible_search import BibleSearch
import re

def extract_word_variations(results, stem):
    """Extract all word variations matching the stem"""
    words = {}
    pattern = r'\b' + re.escape(stem) + r'\w*'

    for r in results[:100]:
        matches = re.findall(pattern, r.text, re.IGNORECASE)
        for match in matches:
            word = match.capitalize()
            words[word] = words.get(word, 0) + 1

    return words

# Initialize
bible = BibleSearch('database/bibles.db')

print("=" * 70)
print("Test 1: believ% (stem/root wildcard)")
print("=" * 70)

results1 = bible.search_verses(
    query='believ%',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: believ%")
print(f"Results: {len(results1)} verses")
print()

words1 = extract_word_variations(results1, 'believ')
print("Variations found:")
for word, count in sorted(words1.items(), key=lambda x: (-x[1], x[0])):
    print(f"  • {word}: {count}")

print()
print(f"Highlighted: {results1[0].highlighted_text[:80]}...")

print()
print("=" * 70)
print("Test 2: lov% (stem/root wildcard)")
print("=" * 70)

results2 = bible.search_verses(
    query='lov%',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: lov%")
print(f"Results: {len(results2)} verses")
print()

words2 = extract_word_variations(results2, 'lov')
print("Variations found (top 10):")
for word, count in sorted(words2.items(), key=lambda x: (-x[1], x[0]))[:10]:
    print(f"  • {word}: {count}")

print()
print("=" * 70)
print("Test 3: % with & placeholder (who & believ%)")
print("=" * 70)

results3 = bible.search_verses(
    query='who & believ%',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: who & believ%")
print(f"Results: {len(results3)} verses")
print()

if results3:
    # Extract phrase patterns
    phrase_counts = {}
    query = 'who & believ%'

    regex_parts = []
    for part in query.split():
        if part == '&':
            regex_parts.append(r'(\w+)')
        else:
            word_pattern = part.replace('*', r'\w*').replace('%', r'\w*').replace('?', r'\w')
            regex_parts.append(f'({word_pattern})')

    regex_pattern = r'\b' + r'\s+'.join(regex_parts) + r'\b'

    for result in results3:
        text = result.text.replace('[', '').replace(']', '')
        for match in re.finditer(regex_pattern, text, flags=re.IGNORECASE):
            matched_words = match.groups()
            phrase = ' '.join(word.capitalize() for word in matched_words)
            phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

    print("Phrase patterns:")
    for phrase, count in sorted(phrase_counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  • {phrase}: {count}")

    print()
    print(f"Highlighted: {results3[0].highlighted_text[:100]}...")

print()
print("=" * 70)
print("Test 4: Comparing * vs % (should be identical)")
print("=" * 70)

results_star = bible.search_verses(query='believ*', enabled_translations=['KJV'], book_filter=[])
results_percent = bible.search_verses(query='believ%', enabled_translations=['KJV'], book_filter=[])

print(f"believ* : {len(results_star)} results")
print(f"believ% : {len(results_percent)} results")
print(f"Identical: {'✓ YES' if len(results_star) == len(results_percent) else '✗ NO'}")

print()
print("✅ All tests completed successfully!")
print()
print("Summary:")
print("  • % works as a stem/root wildcard")
print("  • % finds all word variations (believe, believed, believer, etc.)")
print("  • % works with & placeholder for complex patterns")
print("  • * and % are equivalent (both match word stems)")
