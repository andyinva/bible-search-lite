#!/usr/bin/env python3
"""Test word placeholder (&) functionality"""

from bible_search import BibleSearch

# Initialize BibleSearch
bible = BibleSearch('database/bibles.db')

print("=" * 60)
print("Test 1: Search 'who & send' (should match 'who will send', etc.)")
print("=" * 60)

results = bible.search_verses(
    query='who & send',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Found {len(results)} results")
print()

# Show first 5 results
for i, result in enumerate(results[:5]):
    print(f"{i+1}. {result.book} {result.chapter}:{result.verse}")
    print(f"   {result.highlighted_text}")
    print()

print("=" * 60)
print("Test 2: Search 'who & & send' (should match 'who will then send', etc.)")
print("=" * 60)

results2 = bible.search_verses(
    query='who & & send',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Found {len(results2)} results")
print()

# Show first 5 results
for i, result in enumerate(results2[:5]):
    print(f"{i+1}. {result.book} {result.chapter}:{result.verse}")
    print(f"   {result.highlighted_text}")
    print()

print("=" * 60)
print("Test 3: Search 'who & sen*' (wildcard + placeholder)")
print("=" * 60)

results3 = bible.search_verses(
    query='who & sen*',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Found {len(results3)} results")
print()

# Show first 5 results
for i, result in enumerate(results3[:5]):
    print(f"{i+1}. {result.book} {result.chapter}:{result.verse}")
    print(f"   {result.highlighted_text}")
    print()
