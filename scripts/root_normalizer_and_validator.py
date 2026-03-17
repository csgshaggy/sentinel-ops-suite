#!/usr/bin/env python3
import os
from pathlib import Path
import argparse
import shutil

# ------------------------------------------------------------
# Resolve script directory and project root
# ------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

EXPECTED_DIRS = {
    "archive",
    "bin",
    "docs",
    "scripts",
    "tools",
}

PROTECTED_DIRS = {
    "Desktop", "Documents", "Downloads", "Music",
    "Pictures", "Public", "Videos", "thm"
}

KEEP_FILES = {
    # Python tools
    "ssrf_internal_host_bruteforcer.py",
    "ssrf_internal_route_bruteforce.py",
    "ssrf_param_bruteforce.py",
    "ssrf_discovery.py",
    "ssrf_enum_extract.py",
    "ssrf_probe_extract.py",
    "ssrf_recursive_crawler.py",
    "extract_flag_auto.py",
    "extract_lfi_enum.py",
    "extract_links.py",
    "metadata_extractor.py",
    "pdf_object_dump.py",
    "pdf_object_extractor.py",
    "targetedKerberoast.py",

    # Shell tools
    "subnet_scanner.sh",
    "compare_results.sh",
    "find_anomalies.sh",
    "summarize_results.sh",
    "results_toolkit.sh",
    "connect.sh",
    "git-autosync.sh",
    "git-autosynch.sh",
    "safe_autosync.sh",
    "ssrf_batch.sh",
    "tweaker.sh",
    "view_results.sh",
}

BINARIES = {
    "ssrf-command-center-v3",
    "ssrf-command-console",
    "ssrf-command-console-backup",
    "ssrf-command-console_backup",
    "SSRF_PivotScan",
    "ssrf_results",
    "ssrf_reports",
}

# ------------------------------------------------------------
# Remove empty directories
# ------------------------------------------------------------
def remove_empty_dirs():
    print("\n[1] Checking for empty directories...")
    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and item.name not in PROTECTED_DIRS | EXPECTED_DIRS:
            if not any(item.iterdir()):
                print(f"→ Removing empty directory: {item.name}")
                item.rmdir()

# ------------------------------------------------------------
# Validate project tree
# ------------------------------------------------------------
def validate_tree():
    print("\n[2] Validating project tree...")

    # Check required directories
    for d in EXPECTED_DIRS:
        if not (PROJECT_ROOT / d).exists():
            print(f"⚠ Missing expected directory: {d}")

    # Check for unexpected directories
    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and item.name not in EXPECTED_DIRS and item.name not in PROTECTED_DIRS:
            print(f"⚠ Unexpected directory in root: {item.name}")

    # Check for misplaced KEEP files
    for item in PROJECT_ROOT.iterdir():
        if item.name in KEEP_FILES:
            print(f"❌ ERROR: KEEP file still in root: {item.name}")

    # Check for misplaced binaries
    for item in PROJECT_ROOT.iterdir():
        if item.name in BINARIES:
            print(f"❌ ERROR: Binary still in root: {item.name}")

    print("Validation complete.")

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def run(dry_run=False):
    print(f"Script directory: {SCRIPT_DIR}")
    print(f"Project root:    {PROJECT_ROOT}")

    remove_empty_dirs()
    validate_tree()

    print("\nRoot normalization and validation complete.")

# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize root and validate project tree")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without modifying anything")
    args = parser.parse_args()

    run(dry_run=args.dry_run)
