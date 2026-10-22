#!/usr/bin/env python3
"""
make_public_database.py  -  a copy of bibles.db fit to publish

Bible Search Lite's own database/bibles.db holds every translation,
some of them still under copyright.  That copy is for this computer.
What goes on GitHub (the release downloads that setup.py, setup_win11.py
and DOWNLOAD_DATABASE.md hand out) should hold only the translations
that may be passed on.  This script makes that copy, and leaves
database/bibles.db exactly as it is.

    python3 make_public_database.py
    python3 make_public_database.py --remove JUB,LEB,LIT,MKJ
    python3 make_public_database.py --list

It writes three files into public_release/ (a folder git ignores):

    bibles.db            the database without the removed translations
    bible_data.sql.gz    the same as a compressed SQL dump, the file
                         setup.py downloads and turns into bibles.db
    checksums.txt        the dump's SHA256, which setup.py checks

Upload all three to the release in place of the old ones, under the
same names, and every download link keeps working.

--remove names the translations to leave out, by abbreviation.  Without
it the script leaves out the six Word Atlas treats as under copyright
(JUB, LEB, NET, LIT, MKJ, BBE); name your own list to keep any of those
whose terms allow passing it on.  --list prints every translation in
database/bibles.db with its verse count and stops.

Standard library only (sqlite3, gzip, hashlib), so it runs the same on
Ubuntu and Windows 11 without the sqlite3 or gzip programs.

Author: Andrew Hopkins (with Claude)
"""

import gzip
import hashlib
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "database", "bibles.db")        # the full copy, never changed
OUT_DIR = os.path.join(HERE, "public_release")
# The translations Word Atlas leaves out as under copyright (atlas_source.py)
DEFAULT_REMOVE = ["JUB", "LEB", "NET", "LIT", "MKJ", "BBE"]


def translations(db):
    """Every translation in a database: (id, abbreviation, name, verse count)."""
    rows = db.execute("SELECT t.id, t.abbreviation, t.name, COUNT(vt.verse_id) FROM translations t "
                      "LEFT JOIN verse_texts vt ON vt.translation_id = t.id "
                      "GROUP BY t.id ORDER BY t.abbreviation").fetchall()
    return rows


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def make_public(remove, source=SOURCE, out_dir=OUT_DIR, log=print):
    """
    Write the public bibles.db, its dump and the dump's checksum into
    out_dir, without the translations named in remove.  Returns the
    abbreviations removed and the paths written.
    """
    if not os.path.exists(source):
        raise SystemExit(f"{source} not found: this script runs in Bible Search Lite's folder.")
    os.makedirs(out_dir, exist_ok=True)
    public = os.path.join(out_dir, "bibles.db")
    if os.path.exists(public):
        os.remove(public)

    # 1. A copy of the whole database, made by SQLite itself (safe even
    #    while Bible Search Lite has the file open for reading)
    log(f"Copying {source} ...")
    src = sqlite3.connect("file:" + source.replace("\\", "/") + "?mode=ro", uri=True)
    dst = sqlite3.connect(public)
    src.backup(dst)
    src.close()

    # 2. The translations to leave out: every one named must be there,
    #    so a typing slip cannot leave a translation in by accident
    present = {abbr.upper(): (tid, name) for tid, abbr, name, _ in translations(dst)}
    unknown = [a for a in remove if a.upper() not in present]
    if unknown:
        dst.close()
        os.remove(public)
        raise SystemExit(f"Not in bibles.db: {', '.join(unknown)}.  python3 make_public_database.py --list "
                         f"shows the abbreviations.")
    ids = [present[a.upper()][0] for a in remove]
    marks = ",".join("?" * len(ids))
    for abbr in remove:
        log(f"  removing {abbr.upper()}: {present[abbr.upper()][1]}")
    # Their verses first, then the translations themselves
    dst.execute(f"DELETE FROM verse_texts WHERE translation_id IN ({marks})", ids)
    dst.execute(f"DELETE FROM translations WHERE id IN ({marks})", ids)
    dst.commit()

    # 3. Check: none of their text is left, and every other translation
    #    kept every verse it had
    left = dst.execute(f"SELECT COUNT(*) FROM verse_texts WHERE translation_id IN ({marks})", ids).fetchone()[0]
    if left:
        raise SystemExit(f"{left} verses of the removed translations are still there: nothing is published.")
    log("Compacting ...")
    dst.execute("VACUUM")
    kept = translations(dst)
    log(f"  {len(kept)} translations kept: {', '.join(abbr for _, abbr, _, _ in kept)}")

    # 4. The dump setup.py downloads, written by Python (no sqlite3 or
    #    gzip program needed), then its checksum
    dump = os.path.join(out_dir, "bible_data.sql.gz")
    log(f"Writing {dump} ...")
    with gzip.open(dump, "wt", encoding="utf-8", compresslevel=9) as f:
        for line in dst.iterdump():
            f.write(line + "\n")
    dst.close()
    checksum = sha256(dump)
    checksums = os.path.join(out_dir, "checksums.txt")
    with open(checksums, "w", encoding="utf-8") as f:
        f.write("# SHA256 Checksums for Bible Search Lite Data Files\n")
        f.write("# Generated by make_public_database.py (the public copy, without the translations under copyright)\n\n")
        f.write(f"bible_data.sql.gz: {checksum}\n")

    # 5. The dump read back into a fresh database, as setup.py will do,
    #    and counted: what is published is known to rebuild
    log("Reading the dump back to check it ...")
    # Into a scratch file, one statement at a time, so a dump of several
    # hundred megabytes never has to sit in memory whole
    scratch = os.path.join(out_dir, "check_rebuild.db")
    if os.path.exists(scratch):
        os.remove(scratch)
    check = sqlite3.connect(scratch)
    check.isolation_level = None            # the dump's own BEGIN and COMMIT are obeyed as written
    statement = ""
    with gzip.open(dump, "rt", encoding="utf-8") as f:
        for line in f:
            statement += line
            # A statement can span lines (a verse with a line break in it):
            # run it only once SQLite says it is whole
            if sqlite3.complete_statement(statement):
                check.execute(statement)
                statement = ""
    rebuilt = translations(check)
    check.close()
    os.remove(scratch)
    if [(a, n) for _, a, _, n in rebuilt] != [(a, n) for _, a, _, n in kept]:
        raise SystemExit("The dump does not rebuild the same database: do not publish it.")
    log("")
    log("Written, and checked:")
    for path in (public, dump, checksums):
        log(f"  {path}  ({os.path.getsize(path) / 1e6:.1f} MB)")
    log(f"Removed: {', '.join(a.upper() for a in remove)}.  database/bibles.db is unchanged.")
    log("Next: on the GitHub release, delete the old bibles.db, bible_data.sql.gz and checksums.txt and "
        "upload these three under the same names.")
    return [a.upper() for a in remove], (public, dump, checksums)


def main(argv):
    args = argv[1:]
    if "-h" in args or "--help" in args:
        print(__doc__)
        return 0
    if "--list" in args:
        db = sqlite3.connect("file:" + SOURCE.replace("\\", "/") + "?mode=ro", uri=True)
        for _, abbr, name, count in translations(db):
            mark = "  (left out by default)" if abbr.upper() in DEFAULT_REMOVE else ""
            print(f"  {abbr:6} {count:>7,} verses  {name}{mark}")
        db.close()
        return 0
    remove = DEFAULT_REMOVE
    if "--remove" in args:
        i = args.index("--remove")
        if i + 1 >= len(args):
            print("--remove needs a list: --remove JUB,LEB,LIT,MKJ")
            return 1
        remove = [a.strip() for a in args[i + 1].split(",") if a.strip()]
    make_public(remove)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
