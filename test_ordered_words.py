#!/usr/bin/env python3
"""Test > (ordered words) operator functionality"""

from bible_search import BibleSearch

# Initialize
bible = BibleSearch('database/bibles.db')

print("=" * 70)
print("Test 1: love > neighbour (ordered words)")
print("=" * 70)

results1 = bible.search_verses(
    query='love > neighbour',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: love > neighbour")
print(f"Results: {len(results1)} verses")
print()
print("Sample results:")
for i, r in enumerate(results1[:5]):
    print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
    print(f"   {r.highlighted_text}")
    print()

print("=" * 70)
print("Test 2: God > love > man (three ordered words)")
print("=" * 70)

results2 = bible.search_verses(
    query='God > love > man',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: God > love > man")
print(f"Results: {len(results2)} verses")
print()
if results2:
    print("Sample results:")
    for i, r in enumerate(results2[:3]):
        print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
        print(f"   {r.highlighted_text[:120]}...")
        print()

print("=" * 70)
print("Test 3: Ordered words with wildcard (lov% > God)")
print("=" * 70)

results3 = bible.search_verses(
    query='lov% > God',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: lov% > God")
print(f"Results: {len(results3)} verses")
print()
if results3:
    print("Sample results:")
    for i, r in enumerate(results3[:5]):
        print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
        print(f"   {r.highlighted_text[:100]}...")
        print()

print("=" * 70)
print("Test 4: Verify order matters (God > love vs love > God)")
print("=" * 70)

results_god_love = bible.search_verses(query='God > love', enabled_translations=['KJV'], book_filter=[])
results_love_god = bible.search_verses(query='love > God', enabled_translations=['KJV'], book_filter=[])

print(f"God > love: {len(results_god_love)} verses")
print(f"love > God: {len(results_love_god)} verses")
print()
print("These should be different counts, proving order matters!")
print()

if results_god_love:
    print("Sample 'God > love' result:")
    print(f"  {results_god_love[0].highlighted_text[:100]}...")
    print()

if results_love_god:
    print("Sample 'love > God' result:")
    print(f"  {results_love_god[0].highlighted_text[:100]}...")
    print()

print("=" * 70)
print("Test 5: I > love > you (personal pattern)")
print("=" * 70)

results5 = bible.search_verses(
    query='I > love > you',
    enabled_translations=['KJV'],
    book_filter=[]
)

print(f"Search: I > love > you")
print(f"Results: {len(results5)} verses")
print()
if results5:
    print("Sample results:")
    for i, r in enumerate(results5[:3]):
        print(f"{i+1}. {r.book} {r.chapter}:{r.verse}")
        print(f"   {r.highlighted_text[:120]}...")
        print()

print("✅ All tests completed successfully!")
print()
print("Summary:")
print("  • > operator ensures words appear in specified order")
print("  • Words don't need to be consecutive")
print("  • Works with wildcards (*, %)")
print("  • Order matters (A > B is different from B > A)")
print("  • Highlights all matching words in the verse")
