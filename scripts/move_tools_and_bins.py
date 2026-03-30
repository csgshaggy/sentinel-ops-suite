#!/usr/bin/env python3
import shutil
from pathlib import Path
import argparse

# ------------------------------------------------------------
# Resolve script directory and project root
# ------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

TOOLS_DIR = PROJECT_ROOT / "tools"
BIN_DIR = PROJECT_ROOT / "bin"

TOOLS_DIR.mkdir(exist_ok=True)
BIN_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------
# KEEP: Python tools & shell scripts
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# Console builds → bin/
# ------------------------------------------------------------
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
# Move helper
# ------------------------------------------------------------
def move_item(item: Path, target_dir: Path, dry_run=False):
    target = target_dir / item.name
    print(f"→ MOVE: {item.name} → {target_dir.name}/")

    if not dry_run:
        shutil.move(str(item), str(target))


# ------------------------------------------------------------
# Main logic
# ------------------------------------------------------------
def run(dry_run=False):
    print(f"Script directory: {SCRIPT_DIR}")
    print(f"Project root:    {PROJECT_ROOT}")
    print(f"Tools dir:       {TOOLS_DIR}")
    print(f"Bin dir:         {BIN_DIR}")
    print("Scanning project root...\n")

    for item in PROJECT_ROOT.iterdir():
        # Skip directories we should not touch
        if item.is_dir() and item.name in {
            "tools",
            "bin",
            "scripts",
            "docs",
            "archive",
        }:
            continue

        # Move KEEP tools
        if item.name in KEEP_FILES:
            move_item(item, TOOLS_DIR, dry_run)
            continue

        # Move console binaries
        if item.name in BINARIES:
            move_item(item, BIN_DIR, dry_run)
            continue

    print("\nReorganization complete.")


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move KEEP tools to tools/ and console builds to bin/"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show actions without moving files"
    )
    args = parser.parse_args()

    run(dry_run=args.dry_run)
