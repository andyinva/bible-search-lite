#!/usr/bin/env python3
"""Test filter extraction for 'who sen*' search"""
import re

def extract_patterns(search_term):
    """Simulate the extract_word_counts pattern building"""
    search_patterns = []

    # Split on AND/OR (case insensitive)
    terms = re.split(r'\s+(?:AND|OR)\s+', search_term, flags=re.IGNORECASE)

    # If no AND/OR was found, split on spaces (each word is a separate term)
    if len(terms) == 1 and ' ' in terms[0]:
        terms = terms[0].split()

    for term in terms:
        term = term.strip().strip('"\'')
        if not term:
            continue

        # Convert wildcard * to regex pattern
        pattern = re.escape(term.lower())
        pattern = pattern.replace(r'\*', '.*')
        pattern = r'^' + pattern + r'$'
        search_patterns.append(re.compile(pattern))

    return search_patterns

# Test "who sen*"
search_term = "who sen*"
patterns = extract_patterns(search_term)

print(f"Search: '{search_term}'")
print(f"Patterns: {[p.pattern for p in patterns]}")
print()

# Test words
test_words = ["who", "sent", "send", "sending", "sense", "the", "was", "have"]
print("Word matching:")
for word in test_words:
    word_lower = word.lower()
    matches = any(p.match(word_lower) for p in patterns)
    status = "✓ MATCH" if matches else "✗ no match"
    print(f"  {word:15} {status}")

print("\n" + "="*50)

# Test "who AND sen*"
search_term2 = "who AND sen*"
patterns2 = extract_patterns(search_term2)

print(f"Search: '{search_term2}'")
print(f"Patterns: {[p.pattern for p in patterns2]}")
print()

print("Word matching:")
for word in test_words:
    word_lower = word.lower()
    matches = any(p.match(word_lower) for p in patterns2)
    status = "✓ MATCH" if matches else "✗ no match"
    print(f"  {word:15} {status}")
