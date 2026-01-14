#!/usr/bin/env python3
"""Test script to verify book filter functionality"""

from bible_search import BibleSearch

# Initialize BibleSearch
bible = BibleSearch("database/bibles.db")

# Test 1: Search "love" in All Books
print("=" * 60)
print("Test 1: Search 'love' in All Books")
print("=" * 60)
results = bible.search_verses(
    query="love",
    enabled_translations=["KJV"],
    book_filter=[]  # Empty = all books
)
print(f"Results: {len(results)} verses")
if results:
    print(f"First result: {results[0].book} {results[0].chapter}:{results[0].verse}")
    print(f"Last result: {results[-1].book} {results[-1].chapter}:{results[-1].verse}")

# Test 2: Search "love" in New Testament only
print("\n" + "=" * 60)
print("Test 2: Search 'love' in New Testament")
print("=" * 60)
nt_books = [
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon",
    "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]
results_nt = bible.search_verses(
    query="love",
    enabled_translations=["KJV"],
    book_filter=nt_books
)
print(f"Results: {len(results_nt)} verses")
if results_nt:
    print(f"First result: {results_nt[0].book} {results_nt[0].chapter}:{results_nt[0].verse}")
    print(f"Last result: {results_nt[-1].book} {results_nt[-1].chapter}:{results_nt[-1].verse}")
    # Check if any OT books sneaked in
    ot_results = [r for r in results_nt if r.book not in nt_books]
    if ot_results:
        print(f"ERROR: Found {len(ot_results)} Old Testament results!")
        for r in ot_results[:5]:
            print(f"  - {r.book} {r.chapter}:{r.verse}")
    else:
        print("✓ All results are from New Testament")

# Test 3: Search "love" in Gospels only
print("\n" + "=" * 60)
print("Test 3: Search 'love' in Gospels")
print("=" * 60)
gospels = ["Matthew", "Mark", "Luke", "John"]
results_gospels = bible.search_verses(
    query="love",
    enabled_translations=["KJV"],
    book_filter=gospels
)
print(f"Results: {len(results_gospels)} verses")
if results_gospels:
    print(f"First result: {results_gospels[0].book} {results_gospels[0].chapter}:{results_gospels[0].verse}")
    print(f"Last result: {results_gospels[-1].book} {results_gospels[-1].chapter}:{results_gospels[-1].verse}")
    # Check if any non-gospel books sneaked in
    non_gospel = [r for r in results_gospels if r.book not in gospels]
    if non_gospel:
        print(f"ERROR: Found {len(non_gospel)} non-Gospel results!")
        for r in non_gospel[:5]:
            print(f"  - {r.book} {r.chapter}:{r.verse}")
    else:
        print("✓ All results are from Gospels")
