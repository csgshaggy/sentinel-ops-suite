#!/usr/bin/env python3
"""
Safe auto-create for missing __init__.py files.
Only touches real Python package directories.
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

# Directories that represent actual Python package roots
PACKAGE_ROOTS = [
    REPO_ROOT / "src",
    REPO_ROOT / "app",
    REPO_ROOT / "backend",
    REPO_ROOT / "validators",
    REPO_ROOT / "tools" / "plugins",
]

# Directories that must NEVER be treated as Python packages
IGNORE_DIRS = {
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


def is_ignored(path: Path) -> bool:
    """Return True if this path is inside a directory that should never contain __init__.py."""
    return any(part in IGNORE_DIRS for part in path.parts)


def find_missing_inits():
    """Scan only real package roots and return missing __init__.py paths."""
    missing = []
    for root in PACKAGE_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_dir() and not is_ignored(p):
                init_file = p / "__init__.py"
                if not init_file.exists():
                    missing.append(init_file)
    return missing


def main():
    print("=== Safe Fix Missing __init__.py Files ===")
    missing = find_missing_inits()

    if not missing:
        print("[OK] No missing __init__.py files.")
        return

    for path in missing:
        try:
            path.touch()
            print(f"[CREATED] {path}")
        except PermissionError:
            print(f"[SKIPPED - PERMISSION] {path}")
        except Exception as e:
            print(f"[SKIPPED - ERROR] {path} -> {e}")

    print(f"[DONE] Created {len(missing)} __init__.py files.")


if __name__ == "__main__":
    main()
