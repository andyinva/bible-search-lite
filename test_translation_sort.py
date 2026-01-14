#!/usr/bin/env python3
"""Test translation sorting by date"""

# Translation publication dates
TRANSLATION_DATES = {
    'ACV': '',
    'AKJ': '',
    'AND': '1864',
    'ASV': '1901',
    'BBE': '1949',
    'BIS': '1568',
    'BSB': '2016',
    'BST': '1844',
    'COV': '1535',
    'CPD': '2009',
    'DBT': '1890',
    'DRB': '1582-1610',
    'DRC': '1749-52',
    'ERV': '1881-85',
    'GEN': '1560',
    'GN2': '1599',
    'HAW': '1795',
    'JPS': '1917',
    'JUB': '2000',
    'KJA': '1611',
    'KJV': '1611',
    'KPC': '1900',
    'LEB': '2012',
    'LIT': '1985',
    'MKJ': '1962',
    'NET': '2005',
    'NHE': '2023',
    'NHJ': '2023',
    'NHM': '2023',
    'NOY': '1869',
    'OEB': '2010',
    'OEC': '2010',
    'RLT': '',
    'RNK': '',
    'ROT': '1902',
    'RWB': '1833',
    'TWE': '1904',
    'TYD': '1525',
    'TYN': '1526-30',
    'UKJ': '',
    'WBT': '1833',
    'WEB': '2020',
    'WNT': '1903',
    'WYC': '1382-95',
    'YLT': '1862'
}

# Create mock translation objects
class MockTranslation:
    def __init__(self, abbrev, name):
        self.abbreviation = abbrev
        self.full_name = name

# Get all abbreviations
translations = [MockTranslation(abbrev, abbrev) for abbrev in TRANSLATION_DATES.keys()]

# Sort function
def get_sort_key(translation):
    """
    Returns a sort key for translations.
    Most recent dates first, oldest last, no dates at the end.
    """
    abbrev = translation.abbreviation
    date = TRANSLATION_DATES.get(abbrev, '')

    if not date:
        # No date - sort to end (use year 0)
        return 0

    # Extract year from date string
    # Handle ranges like "1582-1610" by taking the end year
    if '-' in date:
        parts = date.split('-')
        # Get the last part (end year)
        year_str = parts[-1]
    else:
        year_str = date

    try:
        year = int(year_str)
        # Negate to sort most recent first
        return -year
    except ValueError:
        # If we can't parse it, treat as no date
        return 0

# Sort translations
sorted_translations = sorted(translations, key=get_sort_key)

# Display sorted list
print("Translations sorted by date (most recent first):")
print("=" * 60)

for trans in sorted_translations:
    abbrev = trans.abbreviation
    date = TRANSLATION_DATES.get(abbrev, '')
    if date:
        print(f"{abbrev:5} - {date}")
    else:
        print(f"{abbrev:5} - (no date)")

print("=" * 60)
print(f"Total: {len(sorted_translations)} translations")
