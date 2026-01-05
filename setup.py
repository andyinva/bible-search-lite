#!/usr/bin/env python3
"""
setup.py - Bible Search Lite Installer

One-command installer that downloads and sets up Bible Search Lite:
  • Downloads compressed Bible database from GitHub Releases
  • Verifies download integrity with SHA256 checksum
  • Creates SQLite database with all indexes
  • Installs Python dependencies
  • Downloads all application files

Usage:
    python3 setup.py

Requirements:
    • Python 3.7 or higher
    • Internet connection
    • sqlite3 command-line tool
    • gzip utility

Author: Andrew Hopkins
"""

import os
import subprocess
import urllib.request
import urllib.error
import hashlib
import sys
import platform

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

def install_sqlite3():
    """Attempt to install sqlite3 based on the platform"""
    system = platform.system()

    if system == 'Linux':
        # Detect Linux distribution
        try:
            with open('/etc/os-release') as f:
                os_info = f.read().lower()

            if 'debian' in os_info or 'ubuntu' in os_info:
                print("\n  Installing SQLite3 on Debian/Ubuntu...")
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'sqlite3'], check=True)
            elif 'fedora' in os_info or 'rhel' in os_info or 'centos' in os_info:
                print("\n  Installing SQLite3 on Fedora/RHEL/CentOS...")
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'sqlite'], check=True)
            elif 'arch' in os_info:
                print("\n  Installing SQLite3 on Arch Linux...")
                subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'sqlite'], check=True)
            else:
                print("\n  ⚠️  Unknown Linux distribution")
                return False

            return True

        except Exception as e:
            print(f"  ❌ Installation failed: {e}")
            return False

    elif system == 'Darwin':  # macOS
        print("\n  Installing SQLite3 on macOS...")
        try:
            subprocess.run(['brew', 'install', 'sqlite3'], check=True)
            return True
        except Exception as e:
            print(f"  ❌ Installation failed: {e}")
            print("  Note: You may need to install Homebrew first:")
            print("    /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            return False

    else:
        print(f"\n  ⚠️  Automatic installation not supported on {system}")
        return False

def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")

    required_tools = ['sqlite3', 'gunzip']
    missing = []

    for tool in required_tools:
        try:
            subprocess.run([tool, '--version'],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         check=True)
            print(f"  ✅ {tool} found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ❌ {tool} not found")
            missing.append(tool)

    if missing:
        print(f"\n❌ Missing required tools: {', '.join(missing)}")

        # Special handling for sqlite3 - offer to install
        if 'sqlite3' in missing:
            print("\nSQLite3 is required to run Bible Search Lite.")
            response = input("Would you like to install SQLite3 now? (Y/n): ").strip().lower()

            if response == '' or response == 'y' or response == 'yes':
                if install_sqlite3():
                    print("  ✅ SQLite3 installed successfully!")
                    missing.remove('sqlite3')
                else:
                    print("\n  Please install SQLite3 manually:")
                    if platform.system() == 'Linux':
                        print("    sudo apt-get install sqlite3")
                    elif platform.system() == 'Darwin':
                        print("    brew install sqlite3")
            else:
                print("\n  Please install SQLite3 manually before continuing:")
                if platform.system() == 'Linux':
                    print("    sudo apt-get install sqlite3")
                elif platform.system() == 'Darwin':
                    print("    brew install sqlite3")

        # If still missing tools, show instructions and exit
        if missing:
            print(f"\n❌ Still missing: {', '.join(missing)}")
            print("\nPlease install the missing tools:")
            if platform.system() == 'Linux':
                print(f"  sudo apt-get install {' '.join(missing)}")
            elif platform.system() == 'Darwin':
                print(f"  brew install {' '.join(missing)}")
            sys.exit(1)

    print()

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
    with open(checksums_path) as f:
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

    # Decompress
    print("\nDecompressing database...")
    try:
        subprocess.run(['gunzip', '-f', db_compressed_path], check=True)
        db_sql_path = db_compressed_path.replace('.gz', '')
        print(f"  ✅ Decompressed to {db_sql_path}")
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Decompression failed: {e}")
        sys.exit(1)

    # Import to SQLite
    print("\nCreating SQLite database (this may take a few minutes)...")
    db_path = 'database/bibles.db'

    try:
        with open(db_sql_path, 'r') as f:
            subprocess.run(['sqlite3', db_path], stdin=f, check=True)

        db_size_mb = os.path.getsize(db_path) / (1024 * 1024)
        print(f"  ✅ Created {db_path} ({db_size_mb:.1f} MB)")
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Database creation failed: {e}")
        sys.exit(1)

    # Verify database
    print("\nVerifying database...")
    try:
        result = subprocess.run(
            ['sqlite3', db_path, 'SELECT COUNT(*) FROM translations;'],
            capture_output=True,
            text=True,
            check=True
        )
        translation_count = result.stdout.strip()
        print(f"  ✅ Database verified ({translation_count} translations found)")
    except subprocess.CalledProcessError:
        print(f"  ❌ Database verification failed")
        sys.exit(1)

    # Cleanup
    print("\nCleaning up temporary files...")
    try:
        os.remove(db_sql_path)
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

    # Make scripts executable
    if os.path.exists('run_bible_search.sh'):
        os.chmod('run_bible_search.sh', 0o755)
        print("  ✅ Made run_bible_search.sh executable")

    # Create empty database for user data
    print("\nCreating user data database...")
    os.makedirs('database', exist_ok=True)
    subprocess.run(['sqlite3', 'database/subjects.db', '.quit'], check=True)
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

def main():
    """Main installation process"""
    print_header("Bible Search Lite - Setup Installer")

    print(f"This installer will:")
    print(f"  • Download Bible database from GitHub Release {RELEASE_VERSION}")
    print(f"  • Set up SQLite database with all translations")
    print(f"  • Download application files")
    print(f"  • Install Python dependencies")
    print()
    input("Press Enter to continue...")

    try:
        # Check requirements
        check_requirements()

        # Setup database
        setup_database()

        # Download application files
        download_application_files()

        # Install dependencies
        install_dependencies()

        # Success!
        print_header("✅ Installation Complete!")

        print("Bible Search Lite is now installed!")
        print()
        print("To run the application:")
        print("  ./run_bible_search.sh")
        print("  or")
        print("  python3 bible_search_lite.py")
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
