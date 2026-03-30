#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "scripts" / "drift_snapshot.json"

# Directories to ignore entirely
IGNORE_DIRS = {
    "__pycache__",
    ".git",
    ".pytest_cache",
    "pytest_cache",
    "venv",
    "src/ssrf_command_console.egg-info",
}

# File extensions to ignore
IGNORE_EXT = {".pyc", ".pyo", ".pth"}

# Specific files to ignore
IGNORE_FILES = {str(SNAPSHOT.relative_to(ROOT))}


def should_ignore(path: Path) -> bool:
    rel = str(path.relative_to(ROOT))

    # Ignore specific files
    if rel in IGNORE_FILES:
        return True

    # Ignore directories
    if any(part in IGNORE_DIRS for part in path.parts):
        return True

    # Ignore file extensions
    if path.suffix in IGNORE_EXT:
        return True

    # Ignore egg-info directories
    if "egg-info" in path.parts:
        return True

    return False


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    state = {}

    for p in ROOT.rglob("*"):
        if p.is_file() and not should_ignore(p):
            rel = str(p.relative_to(ROOT))
            state[rel] = hash_file(p)

    SNAPSHOT.write_text(json.dumps(state, indent=2))
    print(f"[*] Snapshot updated: {SNAPSHOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
