# Bible Search Lite - Database Schema Documentation

## Database Location
```
/home/ajhinva/projects/bible-search-lite/database/
```

## Database Files

1. **bibles.db** - Main Bible text and cross-reference database
2. **subjects.db** - User-created subjects and collected verses
3. **bibles_backup.db** - Backup of main database
4. **user_data.db** - Additional user data (if used)

---

## Main Database: bibles.db

### Current Statistics
- **66 books** (39 Old Testament, 27 New Testament)
- **39 translations** available
- **32,584 unique verses** (book/chapter/verse combinations)
- **980,606 verse texts** (verses × translations)

---

## Table Schemas

### 1. books
Stores the 66 books of the Bible with metadata.

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                    -- Full name (e.g., "Genesis")
    abbreviation TEXT NOT NULL,            -- 3-letter code (e.g., "Gen")
    testament TEXT NOT NULL,               -- "Old" or "New"
    order_index INTEGER NOT NULL UNIQUE    -- Canonical ordering (1-66)
);
```

**Sample Data:**
| id | name | abbreviation | testament | order_index |
|----|------|--------------|-----------|-------------|
| 1 | Genesis | Gen | Old | 1 |
| 2 | Exodus | Exo | Old | 2 |
| 40 | Matthew | Mat | New | 40 |

**Indexes:**
- `idx_books_abbr` on `abbreviation`

---

### 2. translations
Stores Bible translation metadata.

```sql
CREATE TABLE translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                    -- Full name (e.g., "King James Bible")
    abbreviation TEXT NOT NULL UNIQUE,     -- Short code (e.g., "KJV")
    description TEXT,                      -- Full description
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:**
| id | name | abbreviation | description |
|----|------|--------------|-------------|
| 1 | King James Bible | KJV | King James Version (1611) |
| 2 | American Standard Version | ASV | American Standard Version (1901) |
| 39 | (39 total translations) | ... | ... |

**Indexes:**
- `idx_translations_abbr` on `abbreviation`
- `UNIQUE` constraint on `abbreviation`

---

### 3. verses
Stores unique verse references (book/chapter/verse combinations).

```sql
CREATE TABLE verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,              -- Foreign key to books
    chapter INTEGER NOT NULL,              -- Chapter number
    verse_number INTEGER NOT NULL,         -- Verse number
    FOREIGN KEY (book_id) REFERENCES books(id),
    UNIQUE(book_id, chapter, verse_number) -- One entry per verse
);
```

**Example:**
| id | book_id | chapter | verse_number | Represents |
|----|---------|---------|--------------|------------|
| 1 | 1 | 1 | 1 | Genesis 1:1 |
| 2 | 1 | 1 | 2 | Genesis 1:2 |

**Indexes:**
- `idx_verses_book_chapter` on `(book_id, chapter)`
- `UNIQUE` on `(book_id, chapter, verse_number)`

**Total Records:** 32,584 unique verses

---

### 4. verse_texts
Stores the actual text for each verse in each translation.

```sql
CREATE TABLE verse_texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,             -- Foreign key to verses
    translation_id INTEGER NOT NULL,       -- Foreign key to translations
    text TEXT NOT NULL,                    -- The actual verse text
    FOREIGN KEY (verse_id) REFERENCES verses(id),
    FOREIGN KEY (translation_id) REFERENCES translations(id),
    UNIQUE(verse_id, translation_id)       -- One text per verse per translation
);
```

**Example:**
| id | verse_id | translation_id | text |
|----|----------|----------------|------|
| 1 | 1 | 1 | In the beginning God created the heaven and the earth. |
| 2 | 1 | 2 | In the beginning God created the heavens and the earth. |

**Indexes:**
- `idx_verse_texts_verse` on `verse_id`
- `idx_verse_texts_translation` on `translation_id`
- `idx_verse_texts_composite` on `(translation_id, verse_id)` - **Optimized for searches**
- `UNIQUE` on `(verse_id, translation_id)`

**Total Records:** 980,606 verse texts (32,584 verses × ~30 translations average)

---

### 5. cross_references
Stores cross-reference relationships between verses.

```sql
CREATE TABLE cross_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Source verse (where the cross-reference originates)
    from_reference TEXT NOT NULL,          -- "Genesis 1:1"
    from_text TEXT,                        -- Verse text
    from_book TEXT,                        -- "Genesis"
    from_testament TEXT,                   -- "Old" or "New"
    from_chapter INTEGER,                  -- 1
    from_verse_start INTEGER,              -- 1
    from_verse_end INTEGER,                -- 1 (or higher for ranges)

    -- Target verse (what it references)
    to_reference TEXT NOT NULL,            -- "John 1:1"
    to_text TEXT,                          -- Referenced verse text
    to_book TEXT,                          -- "John"
    to_testament TEXT,                     -- "New"
    to_chapter INTEGER,                    -- 1
    to_verse_start INTEGER,                -- 1
    to_verse_end INTEGER,                  -- 1

    -- Metadata
    relevance_score INTEGER,               -- Higher = stronger relationship
    translation TEXT DEFAULT 'KJV',        -- Translation used
    notes TEXT,                            -- User notes
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_cross_ref_from` on `from_reference`
- `idx_cross_ref_to` on `to_reference`
- `idx_cross_ref_from_book` on `from_book`
- `idx_cross_ref_to_book` on `to_book`
- `idx_cross_ref_score` on `relevance_score`

**Purpose:** Links related verses (e.g., prophecies to fulfillments, parallel passages)

---

### 6. verse_strongs
Stores Strong's concordance numbers and morphology for Greek/Hebrew study.

```sql
CREATE TABLE verse_strongs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,             -- Foreign key to verses
    word_position INTEGER NOT NULL,        -- Position of word in verse
    strongs_number TEXT NOT NULL,          -- Strong's number (e.g., "G1722")
    morphology TEXT,                       -- Grammatical analysis
    word_text TEXT,                        -- The actual word
    FOREIGN KEY (verse_id) REFERENCES verses(id)
);
```

**Indexes:**
- `idx_strongs_verse` on `verse_id`
- `idx_strongs_number` on `strongs_number`
- `idx_strongs_word` on `word_text`

**Purpose:**
- Enables searching by Strong's numbers
- Provides morphological analysis (noun, verb, tense, etc.)
- Links to Greek/Hebrew lexicons

---

## Database Views

### 1. verse_lookup
Convenience view for verse searching with all metadata.

```sql
CREATE VIEW verse_lookup AS
    SELECT
        b.name || ' ' || v.chapter || ':' || v.verse_number as reference,
        v.id as verse_id,
        b.name as book,
        b.testament,
        v.chapter,
        v.verse_number,
        t.abbreviation as translation,
        t.name as translation_name,
        vt.text
    FROM verse_texts vt
    JOIN verses v ON vt.verse_id = v.id
    JOIN books b ON v.book_id = b.id
    JOIN translations t ON vt.translation_id = t.id;
```

**Output Example:**
| reference | verse_id | book | testament | chapter | verse_number | translation | text |
|-----------|----------|------|-----------|---------|--------------|-------------|------|
| Genesis 1:1 | 1 | Genesis | Old | 1 | 1 | KJV | In the beginning... |

**Use:** Primary view for searching and displaying verses

---

### 2. verse_comparison
Aggregates all translations of a verse into one row.

```sql
CREATE VIEW verse_comparison AS
    SELECT
        v.id as verse_id,
        b.name || ' ' || v.chapter || ':' || v.verse_number as reference,
        b.name as book,
        v.chapter,
        v.verse_number,
        GROUP_CONCAT(t.abbreviation || ': ' || vt.text, ' | ') as all_translations
    FROM verses v
    JOIN books b ON v.book_id = b.id
    LEFT JOIN verse_texts vt ON v.id = vt.verse_id
    LEFT JOIN translations t ON vt.translation_id = t.id
    GROUP BY v.id;
```

**Use:** Comparing multiple translations side-by-side

---

### 3. books_summary
Statistics for each book.

```sql
CREATE VIEW books_summary AS
    SELECT
        b.id,
        b.name,
        b.abbreviation,
        b.testament,
        b.order_index,
        COUNT(DISTINCT v.id) as total_verses,
        MAX(v.chapter) as total_chapters
    FROM books b
    LEFT JOIN verses v ON b.id = v.book_id
    GROUP BY b.id
    ORDER BY b.order_index;
```

**Output Example:**
| name | abbreviation | testament | total_verses | total_chapters |
|------|--------------|-----------|--------------|----------------|
| Genesis | Gen | Old | 1,533 | 50 |
| Exodus | Exo | Old | 1,213 | 40 |

---

### 4. translation_stats
Coverage statistics for each translation.

```sql
CREATE VIEW translation_stats AS
    SELECT
        t.id,
        t.name,
        t.abbreviation,
        COUNT(vt.id) as verse_count,
        ROUND(COUNT(vt.id) * 100.0 / (SELECT COUNT(*) FROM verses), 2) as coverage_percent
    FROM translations t
    LEFT JOIN verse_texts vt ON t.id = vt.translation_id
    GROUP BY t.id
    ORDER BY verse_count DESC;
```

**Use:** Shows which translations are complete vs partial

---

### 5. verse_search
Optimized view for search operations.

```sql
CREATE VIEW verse_search AS
    SELECT
        v.id as verse_id,
        b.name as book_name,
        b.abbreviation as book_abbr,
        b.testament,
        v.chapter,
        v.verse_number,
        b.name || ' ' || v.chapter || ':' || v.verse_number as full_reference,
        vt.translation_id,
        t.abbreviation as translation,
        vt.text
    FROM verses v
    JOIN books b ON v.book_id = b.id
    JOIN verse_texts vt ON v.id = vt.verse_id
    JOIN translations t ON vt.translation_id = t.id;
```

**Use:** Primary view used by search engine

---

## Subjects Database: subjects.db

### 1. subjects
User-created subject categories.

```sql
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,             -- Subject name (e.g., "Prayer")
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_subjects_name` on `name`
- `UNIQUE` constraint on `name`

**Example:**
| id | name | created_date |
|----|------|--------------|
| 1 | Prayer | 2025-01-15 10:30:00 |
| 2 | Faith | 2025-01-16 14:22:00 |

---

### 2. subject_verses
Verses collected under each subject.

```sql
CREATE TABLE subject_verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,           -- Foreign key to subjects
    verse_reference TEXT NOT NULL,         -- "Genesis 1:1"
    verse_text TEXT NOT NULL,              -- Full verse text
    translation TEXT NOT NULL,             -- "KJV", "NIV", etc.
    comments TEXT DEFAULT '',              -- User comments/notes
    order_index INTEGER DEFAULT 0,         -- Custom ordering
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
    UNIQUE(subject_id, verse_reference, translation)
);
```

**Indexes:**
- `idx_subject_verses_subject_id` on `subject_id`
- `idx_subject_verses_order` on `(subject_id, order_index)`
- `UNIQUE` on `(subject_id, verse_reference, translation)`

**Example:**
| id | subject_id | verse_reference | verse_text | translation | comments |
|----|------------|-----------------|------------|-------------|----------|
| 1 | 1 | Matthew 6:9 | Our Father which art in heaven... | KJV | Lord's Prayer |
| 2 | 1 | Luke 11:1 | Lord, teach us to pray... | KJV | Disciples ask |

**Features:**
- Supports multiple translations of same verse
- User can add comments/notes to each verse
- Custom ordering via `order_index`
- Cascade delete: deleting subject removes all its verses

---

## Entity Relationship Diagram

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   books     │         │   verses    │         │ verse_texts  │
├─────────────┤         ├─────────────┤         ├──────────────┤
│ id (PK)     │────1:N──│ id (PK)     │────1:N──│ id (PK)      │
│ name        │         │ book_id (FK)│         │ verse_id (FK)│
│ abbreviation│         │ chapter     │         │ translation_id│
│ testament   │         │ verse_number│         │ text         │
│ order_index │         └─────────────┘         └──────────────┘
└─────────────┘                                         │
                                                        │
                                                        │1:N
                                                        ▼
                                                ┌──────────────┐
                                                │ translations │
                                                ├──────────────┤
                                                │ id (PK)      │
                                                │ name         │
                                                │ abbreviation │
                                                │ description  │
                                                └──────────────┘

┌─────────────┐                                ┌──────────────────┐
│ verse_      │                                │ cross_references │
│ strongs     │                                ├──────────────────┤
├─────────────┤                                │ id (PK)          │
│ id (PK)     │                                │ from_reference   │
│ verse_id (FK)│───────────────────────────────│ to_reference     │
│ word_position│                                │ relevance_score  │
│ strongs_num │                                │ notes            │
│ morphology  │                                └──────────────────┘
│ word_text   │
└─────────────┘

SUBJECTS DATABASE (subjects.db):

┌─────────────┐         ┌──────────────────┐
│  subjects   │         │ subject_verses   │
├─────────────┤         ├──────────────────┤
│ id (PK)     │────1:N──│ id (PK)          │
│ name (UQ)   │         │ subject_id (FK)  │
│ created_date│         │ verse_reference  │
│ modified_date│        │ verse_text       │
└─────────────┘         │ translation      │
                        │ comments         │
                        │ order_index      │
                        └──────────────────┘
```

---

## Key Relationships

1. **books → verses** (1:N)
   - One book contains many verses
   - Cascade delete: removing a book removes all its verses

2. **verses → verse_texts** (1:N)
   - One verse has many translations (texts)
   - Each translation is a separate row

3. **translations → verse_texts** (1:N)
   - One translation covers many verses
   - Enables filtering by translation

4. **verses → verse_strongs** (1:N)
   - One verse has many words with Strong's numbers
   - Enables concordance and morphology searches

5. **subjects → subject_verses** (1:N with CASCADE)
   - One subject contains many verses
   - Deleting subject deletes all collected verses

---

## Search Optimization

### Primary Search Index
```sql
CREATE INDEX idx_verse_texts_composite
    ON verse_texts(translation_id, verse_id);
```

This composite index enables fast searches by:
1. Filtering by selected translations first
2. Then scanning verse texts within those translations

### Full-Text Search Strategy
The application uses Python-level regex/wildcard matching rather than SQLite FTS because:
- Supports complex wildcard patterns (`*`, `?`, `%`)
- Enables two-color highlighting (base + variation)
- Supports special operators (`~N`, `>`, `&`)
- Better control over matching logic

---

## Performance Characteristics

### Database Size
- **bibles.db**: ~500 MB (with 39 translations)
- **subjects.db**: Small (grows with user data)

### Query Performance
- **Simple searches**: < 100ms (using indexed views)
- **Wildcard searches**: 200-500ms (full scan with Python regex)
- **Multi-translation**: Linear with number of translations selected
- **Cross-references**: Fast (fully indexed on both directions)

### Bottlenecks
1. **Wildcard searches** - Must scan all matching verses (no pre-indexing)
2. **Large result sets** - Limited to 300 displayed at once (Load More button)
3. **Multiple translations** - Linear multiplication (10 translations = 10× data)

### Optimizations Applied
- Composite indexes on high-traffic columns
- Views for common queries (verse_lookup, verse_search)
- Lazy loading (Load More pagination)
- Result caching for Filter dialog
- Book filtering to reduce search space

---

## Database Maintenance

### Backup Strategy
- Automatic backups: `bibles_backup.db`, `bibles_bk.db`
- Subject backups: `subjects_BK.db`

### Integrity Checks
```sql
PRAGMA integrity_check;
PRAGMA foreign_key_check;
```

### Vacuum (Defragment)
```sql
VACUUM;
```

### Statistics Update
```sql
ANALYZE;
```

---

## Future Enhancements

### Potential Additions
1. **Full-Text Search Index** (SQLite FTS5)
   - Would speed up simple keyword searches
   - Trade-off: Larger database, less control over wildcards

2. **Verse Metadata Table**
   - Red letter (words of Jesus)
   - Poetry/prose formatting
   - Section headings

3. **User Bookmarks/Highlights**
   - Personal verse annotations
   - Highlighting colors
   - Reading history

4. **Greek/Hebrew Text Tables**
   - Septuagint (LXX) - Greek Old Testament
   - Hebrew Masoretic Text
   - Greek New Testament (SBLGNT)

5. **Commentary Tables**
   - Link verses to commentaries
   - Study notes
   - Theological references

---

## SQL Query Examples

### Find all verses containing "love" in KJV
```sql
SELECT * FROM verse_lookup
WHERE translation = 'KJV'
  AND text LIKE '%love%'
ORDER BY verse_id;
```

### Compare Genesis 1:1 across all translations
```sql
SELECT translation, text
FROM verse_lookup
WHERE reference = 'Genesis 1:1'
ORDER BY translation;
```

### Get all verses in a subject
```sql
SELECT sv.verse_reference, sv.verse_text, sv.comments
FROM subject_verses sv
JOIN subjects s ON sv.subject_id = s.id
WHERE s.name = 'Prayer'
ORDER BY sv.order_index;
```

### Find cross-references from John 3:16
```sql
SELECT to_reference, to_text, relevance_score
FROM cross_references
WHERE from_reference = 'John 3:16'
ORDER BY relevance_score DESC;
```

### Count verses per book in KJV
```sql
SELECT b.name, COUNT(*) as verse_count
FROM verse_texts vt
JOIN verses v ON vt.verse_id = v.id
JOIN books b ON v.book_id = b.id
JOIN translations t ON vt.translation_id = t.id
WHERE t.abbreviation = 'KJV'
GROUP BY b.name
ORDER BY b.order_index;
```

---

## Conclusion

The Bible Search Lite database is well-structured with:
- ✅ Normalized design (no data redundancy)
- ✅ Comprehensive indexing for performance
- ✅ Foreign key constraints for data integrity
- ✅ Useful views for common queries
- ✅ Support for advanced features (cross-refs, Strong's, subjects)
- ✅ User data separation (subjects.db)

The schema supports current features and is extensible for future enhancements like Greek/Hebrew texts, commentaries, and full-text search.
