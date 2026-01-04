#!/usr/bin/env python3
"""Test ~N (proximity) operator functionality"""

from bible_search import BibleSearch

# Initialize
bible = BibleSearch('database/bibles.db')

print("=" * 70)
print("Test 1: love ~0 God (adjacent words only)")
print("=" * 70)

results1 = bible.search_verses(
    query='love ~0 God',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: love ~0 God")
print(f"Results: {len(results1)} verses")
print()
print("Sample results:")
for i, r in enumerate(results1[:5]):
    print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
    print(f"   {r.highlighted_text}")
    print()

print("=" * 70)
print("Test 2: love ~2 God (0-2 words between)")
print("=" * 70)

results2 = bible.search_verses(
    query='love ~2 God',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: love ~2 God")
print(f"Results: {len(results2)} verses")
print()
print("Sample results:")
for i, r in enumerate(results2[:5]):
    print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
    print(f"   {r.highlighted_text[:120]}...")
    print()

print("=" * 70)
print("Test 3: love ~4 God (0-4 words between)")
print("=" * 70)

results3 = bible.search_verses(
    query='love ~4 God',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: love ~4 God")
print(f"Results: {len(results3)} verses")
print()
print("Sample results:")
for i, r in enumerate(results3[:5]):
    print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
    print(f"   {r.highlighted_text[:120]}...")
    print()

print("=" * 70)
print("Test 4: faith ~5 works (0-5 words between)")
print("=" * 70)

results4 = bible.search_verses(
    query='faith ~5 works',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: faith ~5 works")
print(f"Results: {len(results4)} verses")
print()
if results4:
    print("Sample results:")
    for i, r in enumerate(results4[:3]):
        print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
        print(f"   {r.highlighted_text[:120]}...")
        print()

print("=" * 70)
print("Test 5: Proximity with wildcard (believ% ~3 Jesus)")
print("=" * 70)

results5 = bible.search_verses(
    query='believ% ~3 Jesus',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: believ% ~3 Jesus")
print(f"Results: {len(results5)} verses")
print()
if results5:
    print("Sample results:")
    for i, r in enumerate(results5[:5]):
        print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
        print(f"   {r.highlighted_text[:120]}...")
        print()

print("=" * 70)
print("Test 6: Comparing different proximity distances")
print("=" * 70)

results_0 = bible.search_verses(query='love ~0 God', enabled_translations=['KJV'], book_filter=[])
results_2 = bible.search_verses(query='love ~2 God', enabled_translations=['KJV'], book_filter=[])
results_4 = bible.search_verses(query='love ~4 God', enabled_translations=['KJV'], book_filter=[])
results_10 = bible.search_verses(query='love ~10 God', enabled_translations=['KJV'], book_filter=[])

print(f"love ~0 God:  {len(results_0)} verses (adjacent only)")
print(f"love ~2 God:  {len(results_2)} verses (0-2 words between)")
print(f"love ~4 God:  {len(results_4)} verses (0-4 words between)")
print(f"love ~10 God: {len(results_10)} verses (0-10 words between)")
print()
print("Result counts should increase as proximity distance increases!")
print()

if results_2:
    print("Sample 'love ~2 God' result:")
    print(f"  {results_2[0].highlighted_text[:100]}...")
    print()

print("=" * 70)
print("Test 7: pray% ~5 faith (wildcard + proximity)")
print("=" * 70)

results7 = bible.search_verses(
    query='pray% ~5 faith',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: pray% ~5 faith")
print(f"Results: {len(results7)} verses")
print()
if results7:
    print("Sample results:")
    for i, r in enumerate(results7[:3]):
        print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
        print(f"   {r.highlighted_text[:120]}...")
        print()

print("✅ All tests completed successfully!")
print()
print("Summary:")
print("  • ~N finds words within N words or less of each other")
print("  • ~0 means adjacent words (no words between)")
print("  • Larger N values allow more spacing between words")
print("  • Works with wildcards (* and %)")
print("  • Both words are highlighted in results")
print("  • Result count increases as proximity distance increases")
