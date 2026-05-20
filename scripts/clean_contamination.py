#!/usr/bin/env python3
import os
import re
import shutil
import argparse

# Pattern that identifies the start of the contamination block
CONTAM_PATTERN = re.compile(r"""edge_all_open_tabs\s*=\s*

\[""", re.IGNORECASE)

def read_file_safely(path):
    """
    Try UTF-8 first. If it fails, fall back to Latin-1 so we can still scan.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines(), "utf-8"
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1") as f:
            return f.readlines(), "latin-1"


def clean_file(path, dry_run=False, create_backup=False):
    lines, encoding_used = read_file_safely(path)

    cleaned = []
    contaminated = False

    for line in lines:
        if CONTAM_PATTERN.search(line):
            contaminated = True
            break
        cleaned.append(line)

    if not contaminated:
        return False

    print(f"[FOUND] Contamination in: {path} (encoding={encoding_used})")

    if dry_run:
        print("        → Dry run: would clean this file.")
        return True

    if create_backup:
        backup_path = path + ".bak"
        shutil.copy2(path, backup_path)
        print(f"        → Backup created: {backup_path}")

    # Always write back as UTF-8
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(cleaned)

    print(f"[CLEANED] {path}")
    return True


def walk(root, dry_run=False, create_backup=False):
    print(f"Scanning for contamination… (dry_run={dry_run}, backup={create_backup})")
    changed = 0

    for root_dir, dirs, files in os.walk(root):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root_dir, file)
                if clean_file(full_path, dry_run=dry_run, create_backup=create_backup):
                    changed += 1

    print(f"\nCompleted. Files affected: {changed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean Edge-tab contamination from Python files.")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run).")
    parser.add_argument("--backup", action="store_true", help="Create .bak backups before modifying.")
    parser.add_argument("--root", default=".", help="Root directory to scan (default: current directory).")

    args = parser.parse_args()

    walk(
        root=args.root,
        dry_run=not args.apply,
        create_backup=args.backup
    )
