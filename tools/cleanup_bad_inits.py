#!/usr/bin/env python3
"""
Cleanup script to remove incorrect __init__.py files created in non-package directories.
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

# Directories that should NEVER contain __init__.py
BAD_DIRS = {
    ".git",
    ".github",
    "venv",
    "__pycache__",
    "runtime",
    "docs",
    "bin",
    "deploy",
    "templates",
    "config",
    "data",
    "ops",
    "mk",
    "legacy",
    "logs",
}

GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
NC = "\033[0m"


def info(msg):
    print(f"{YELLOW}[INFO]{NC} {msg}")


def success(msg):
    print(f"{GREEN}[OK]{NC} {msg}")


def warn(msg):
    print(f"{RED}[WARN]{NC} {msg}")


def is_bad_path(path: Path) -> bool:
    return any(part in BAD_DIRS for part in path.parts)


def find_bad_inits():
    bad_files = []
    for p in REPO_ROOT.rglob("__init__.py"):
        if is_bad_path(p.parent):
            bad_files.append(p)
    return bad_files


def main():
    print("=== Cleanup Incorrect __init__.py Files ===")

    bad_files = find_bad_inits()

    if not bad_files:
        success("No incorrect __init__.py files found.")
        return

    for f in bad_files:
        try:
            f.unlink()
            success(f"Removed: {f}")
        except PermissionError:
            warn(f"Permission denied, skipping: {f}")
        except Exception as e:
            warn(f"Failed to remove {f}: {e}")

    print(f"{GREEN}[DONE]{NC} Removed {len(bad_files)} incorrect __init__.py files.")


if __name__ == "__main__":
    main()
