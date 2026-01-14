#!/usr/bin/env python3
"""Test filter pattern matching"""
import re

def test_pattern_matching():
    # Test search term: "sen*"
    search_term = "sen*"

    # Convert to regex
    pattern = re.escape(search_term.lower())
    pattern = pattern.replace(r'\*', '.*')
    pattern = r'^' + pattern + r'$'
    regex = re.compile(pattern)

    print(f"Search term: '{search_term}'")
    print(f"Regex pattern: {pattern}")
    print()

    # Test words
    test_words = [
        "sent", "send", "sending", "sense", "sensible", "sentence",
        "who", "the", "and", "was", "have", "been"
    ]

    print("Testing words:")
    for word in test_words:
        matches = regex.match(word.lower())
        status = "✓ MATCH" if matches else "✗ no match"
        print(f"  {word:15} {status}")
    print()

    # Test two-word search: "who AND sen*"
    print("=" * 50)
    search_term2 = "who AND sen*"
    terms = re.split(r'\s+(?:AND|OR)\s+', search_term2, flags=re.IGNORECASE)

    patterns = []
    for term in terms:
        term = term.strip()
        pattern = re.escape(term.lower())
        pattern = pattern.replace(r'\*', '.*')
        pattern = r'^' + pattern + r'$'
        patterns.append(re.compile(pattern))

    print(f"Search term: '{search_term2}'")
    print(f"Patterns: {[p.pattern for p in patterns]}")
    print()

    print("Testing words:")
    for word in test_words:
        matches_any = any(p.match(word.lower()) for p in patterns)
        status = "✓ MATCH" if matches_any else "✗ no match"
        print(f"  {word:15} {status}")

if __name__ == "__main__":
    test_pattern_matching()
