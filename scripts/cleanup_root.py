#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
import argparse

# ------------------------------------------------------------
# Resolve project root and archive directory
# ------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ARCHIVE_DIR = PROJECT_ROOT / "archive"

# Directories that must NEVER be touched
PROTECTED_DIRS = {
    "Desktop", "Documents", "Downloads", "Music",
    "Pictures", "Public", "Videos", "thm"
}

# Files and patterns safe to archive
SAFE_PATTERNS = [
    "ssrf_*.html",
    "ssrf_host_*.html",
    "ssrf_param_*.html",
    "ssrf_pdf_*.html",
    "ssrf_*.txt.html",
    "ssrf_*.pdf.html",
    "dummy*.pdf",
    "pdf_unpacked.pdf",
    "payload*",
    "cvt*",
    "stream*.zlib",
    "out",
    "out1",
    "out2",
    "out3",
    "part*.txt",
    "extract.txt",
    "extract_lfi_enum.txt",
    "first60.txt",
    "needed_results.txt",
    "results*.txt",
    "param_test_results.txt",
    "site_endpoints.txt",
    "TryHackMeVA.ovpn",
    "ssrf_batch.sh.save*",
]

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def matches_any_pattern(path: Path):
    from fnmatch import fnmatch
    return any(fnmatch(path.name, pattern) for pattern in SAFE_PATTERNS)

def should_archive(path: Path):
    if path.is_dir():
        return False
    if path.name in PROTECTED_DIRS:
        return False
    return matches_any_pattern(path)

# ------------------------------------------------------------
# Main cleanup logic
# ------------------------------------------------------------
def run_cleanup(dry_run=False):
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Archive dir:  {ARCHIVE_DIR}")

    ARCHIVE_DIR.mkdir(exist_ok=True)

    for item in PROJECT_ROOT.iterdir():
        if item.name in PROTECTED_DIRS:
            continue
        if should_archive(item):
            target = ARCHIVE_DIR / item.name
            print(f"→ ARCHIVE: {item.name}")

            if not dry_run:
                shutil.move(str(item), str(target))

    print("Cleanup complete.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Archive safe-to-remove SSRF artifacts.")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without moving files")
    args = parser.parse_args()

    run_cleanup(dry_run=args.dry_run)
