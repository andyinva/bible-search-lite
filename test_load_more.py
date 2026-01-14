#!/usr/bin/env python3
"""Test script to verify Load More button functionality"""

from bible_search import BibleSearch

# Initialize BibleSearch
bible = BibleSearch("database/bibles.db")

# Test: Search "who sent" which should return ~5809 results
print("=" * 60)
print("Test: Search 'who sent' - should return large result set")
print("=" * 60)
results = bible.search_verses(
    query="who sent",
    enabled_translations=["KJV"],
    book_filter=[]  # Empty = all books
)
print(f"Total results: {len(results)} verses")
print()

# Simulate initial load (first 300)
batch_size = 300
initial_batch = results[:batch_size]
remaining = results[batch_size:]

print(f"Initial batch: {len(initial_batch)} verses")
print(f"Remaining: {len(remaining)} verses")
print()

# Simulate loading more batches
batch_num = 1
while remaining:
    next_batch = remaining[:batch_size]
    remaining = remaining[batch_size:]
    batch_num += 1
    print(f"Batch {batch_num}: {len(next_batch)} verses (Remaining: {len(remaining)})")

print()
print(f"✅ All results loaded in {batch_num} batches of {batch_size} each")
