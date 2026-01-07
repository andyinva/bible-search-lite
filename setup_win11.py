#!/usr/bin/env python3
"""
setup_win11.py - Bible Search Lite Installer for Windows 11

Native Windows installer that uses pure Python (no Unix tools required).
Works on Windows 10/11 without WSL2.

Usage:
    python setup_win11.py

Requirements:
    • Python 3.7 or higher
    • Internet connection

Author: Andrew Hopkins
"""

import os
import subprocess
import urllib.request
import urllib.error
import hashlib
import sys
import platform
import gzip
import shutil
import sqlite3

# Configuration
GITHUB_USER = "andyinva"
GITHUB_REPO = "bible-search-lite"
RELEASE_VERSION = "v1.0"  # Update this to match your release tag

# GitHub URLs
RELEASE_BASE_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/releases/download/{RELEASE_VERSION}"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70 + "\n")

def check_python_version():
    """Check if Python version is sufficient"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"  ❌ Python 3.7+ required, found {version.major}.{version.minor}")
        print("     Download Python from: https://www.python.org/downloads/")
        return False
    print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def download_file(url, dest, description=None):
    """Download a file with progress indication"""
    if description is None:
        description = os.path.basename(dest)

    print(f"Downloading {description}...")

    try:
        def reporthook(count, block_size, total_size):
            if total_size > 0:
                percent = int(count * block_size * 100 / total_size)
                sys.stdout.write(f"\r  Progress: {percent}%")
                sys.stdout.flush()

        urllib.request.urlretrieve(url, dest, reporthook)
        print()  # New line after progress

        file_size_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"  ✅ Downloaded {description} ({file_size_mb:.1f} MB)")
        return True

    except urllib.error.URLError as e:
        print(f"\n  ❌ Download failed: {e}")
        print(f"     URL: {url}")
        return False
    except Exception as e:
        print(f"\n  ❌ Error: {e}")
        return False

def verify_checksum(file_path, expected_checksum):
    """Verify file integrity using SHA256"""
    print(f"Verifying {os.path.basename(file_path)}...")

    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)

    actual_checksum = sha256_hash.hexdigest()

    if actual_checksum == expected_checksum:
        print(f"  ✅ Checksum verified")
        return True
    else:
        print(f"  ❌ Checksum mismatch!")
        print(f"     Expected: {expected_checksum}")
        print(f"     Actual:   {actual_checksum}")
        return False

def decompress_gzip(input_file, output_file):
    """Decompress a gzip file using Python's gzip module"""
    print(f"Decompressing {os.path.basename(input_file)}...")

    try:
        with gzip.open(input_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        output_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"  ✅ Decompressed to {os.path.basename(output_file)} ({output_size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"  ❌ Decompression failed: {e}")
        return False

def import_sql_to_sqlite(sql_file, db_path):
    """Import SQL dump into SQLite database using Python sqlite3 module"""
    print(f"Creating SQLite database (this may take a few minutes)...")

    try:
        # Read SQL file
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Create database and execute SQL
        conn = sqlite3.connect(db_path)
        conn.executescript(sql_script)
        conn.close()

        db_size_mb = os.path.getsize(db_path) / (1024 * 1024)
        print(f"  ✅ Created {db_path} ({db_size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"  ❌ Database creation failed: {e}")
        return False

def setup_database():
    """Download and setup the Bible SQLite database"""
    print_header("Step 1: Database Setup")

    # Create directories
    os.makedirs('database', exist_ok=True)
    os.makedirs('temp', exist_ok=True)

    # Download checksums file
    checksums_url = f"{RELEASE_BASE_URL}/checksums.txt"
    checksums_path = "temp/checksums.txt"

    if not download_file(checksums_url, checksums_path, "checksums.txt"):
        print("\n❌ Failed to download checksums file")
        print(f"   Make sure release {RELEASE_VERSION} exists with checksums.txt")
        sys.exit(1)

    # Read expected checksum
    print("\nReading checksums...")
    with open(checksums_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = line.strip().split(': ')
                if len(parts) == 2 and parts[0] == 'bible_data.sql.gz':
                    expected_checksum = parts[1]
                    print(f"  Expected checksum: {expected_checksum[:16]}...")
                    break
        else:
            print("  ❌ Could not find checksum for bible_data.sql.gz")
            sys.exit(1)

    # Download compressed database
    print()
    db_url = f"{RELEASE_BASE_URL}/bible_data.sql.gz"
    db_compressed_path = "temp/bible_data.sql.gz"

    if not download_file(db_url, db_compressed_path, "Bible database (compressed)"):
        print("\n❌ Failed to download database")
        print(f"   Make sure release {RELEASE_VERSION} has bible_data.sql.gz uploaded")
        sys.exit(1)

    # Verify checksum
    print()
    if not verify_checksum(db_compressed_path, expected_checksum):
        print("\n❌ Download verification failed!")
        print("   The file may be corrupted. Please try again.")
        sys.exit(1)

    # Decompress using Python's gzip module
    print()
    db_sql_path = "temp/bible_data.sql"
    if not decompress_gzip(db_compressed_path, db_sql_path):
        sys.exit(1)

    # Import to SQLite using Python's sqlite3 module
    print()
    db_path = 'database/bibles.db'
    if not import_sql_to_sqlite(db_sql_path, db_path):
        sys.exit(1)

    # Verify database
    print("\nVerifying database...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM translations;')
        translation_count = cursor.fetchone()[0]
        conn.close()
        print(f"  ✅ Database verified ({translation_count} translations found)")
    except Exception as e:
        print(f"  ❌ Database verification failed: {e}")
        sys.exit(1)

    # Cleanup
    print("\nCleaning up temporary files...")
    try:
        os.remove(db_sql_path)
        os.remove(db_compressed_path)
        os.remove(checksums_path)
        print("  ✅ Temporary files removed")
    except Exception as e:
        print(f"  ⚠️  Warning: Could not remove temp files: {e}")

def download_application_files():
    """Download application source files from GitHub"""
    print_header("Step 2: Download Application Files")

    # Files to download from the main branch
    files = [
        'bible_search_lite.py',
        'bible_search.py',
        'bible_search_service.py',
        'subject_manager.py',
        'subject_verse_manager.py',
        'subject_comment_manager.py',
        'run_bible_search.sh',
        'README.md',
        'SEARCH_OPERATORS.md',
    ]

    # Directories to create
    directories = [
        'bible_search_ui',
        'bible_search_ui/ui',
        'bible_search_ui/config',
        'bible_search_ui/controllers',
    ]

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Download UI files
    ui_files = [
        'bible_search_ui/__init__.py',
        'bible_search_ui/ui/__init__.py',
        'bible_search_ui/ui/widgets.py',
        'bible_search_ui/ui/dialogs.py',
        'bible_search_ui/config/__init__.py',
        'bible_search_ui/config/config_manager.py',
        'bible_search_ui/controllers/__init__.py',
        'bible_search_ui/controllers/search_controller.py',
    ]

    all_files = files + ui_files

    success_count = 0
    fail_count = 0

    for file_path in all_files:
        url = f"{RAW_BASE_URL}/{file_path}"

        if download_file(url, file_path):
            success_count += 1
        else:
            fail_count += 1
            print(f"  ⚠️  Warning: Could not download {file_path}")

    print(f"\nDownload summary: {success_count} succeeded, {fail_count} failed")

    # Create empty database for user data
    print("\nCreating user data database...")
    os.makedirs('database', exist_ok=True)
    conn = sqlite3.connect('database/subjects.db')
    conn.close()
    print("  ✅ Created database/subjects.db")

def install_dependencies():
    """Install Python dependencies"""
    print_header("Step 3: Install Python Dependencies")

    dependencies = ['PyQt6']

    print("Installing dependencies with pip...")
    for dep in dependencies:
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', dep],
                check=True,
                stdout=subprocess.DEVNULL
            )
            print(f"  ✅ Installed {dep}")
        except subprocess.CalledProcessError:
            print(f"  ❌ Failed to install {dep}")
            print("     You may need to install it manually:")
            print(f"       pip install {dep}")

def create_launcher():
    """Create Windows batch file launcher"""
    print("\nCreating Windows launcher...")

    launcher_content = f"""@echo off
REM Bible Search Lite Launcher for Windows
REM Generated by setup_win11.py

echo Starting Bible Search Lite...
"{sys.executable}" bible_search_lite.py
pause
"""

    try:
        with open('run_bible_search.bat', 'w') as f:
            f.write(launcher_content)
        print("  ✅ Created run_bible_search.bat")
    except Exception as e:
        print(f"  ⚠️  Warning: Could not create launcher: {e}")

def main():
    """Main installation process"""
    print_header("Bible Search Lite - Windows 11 Installer")

    # Check platform
    if platform.system() != 'Windows':
        print("⚠️  This installer is for Windows only.")
        print("   For Linux/macOS, use: python3 setup.py")
        sys.exit(1)

    print(f"This installer will:")
    print(f"  • Download Bible database from GitHub Release {RELEASE_VERSION}")
    print(f"  • Set up SQLite database with all translations")
    print(f"  • Download application files")
    print(f"  • Install Python dependencies")
    print(f"  • Create Windows launcher")
    print()
    input("Press Enter to continue...")

    try:
        # Check Python version
        if not check_python_version():
            sys.exit(1)
        print()

        # Setup database
        setup_database()

        # Download application files
        download_application_files()

        # Install dependencies
        install_dependencies()

        # Create launcher
        create_launcher()

        # Success!
        print_header("✅ Installation Complete!")

        print("Bible Search Lite is now installed!")
        print()
        print("To run the application:")
        print("  • Double-click: run_bible_search.bat")
        print("  or")
        print(f"  • Run: python bible_search_lite.py")
        print()
        print("For help and documentation, see:")
        print("  • README.md - Comprehensive documentation")
        print("  • SEARCH_OPERATORS.md - Search operator reference")
        print()
        print("Enjoy studying the Bible! 📖")
        print()

    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Installation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
