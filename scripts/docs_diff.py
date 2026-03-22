#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
SNAPSHOT_DIR = PROJECT_ROOT / ".docs_snapshots"
SNAPSHOT_FILE = SNAPSHOT_DIR / "latest.json"

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def snapshot_docs():
    data = {}
    for path in DOCS_DIR.rglob("*.md"):
        data[str(path.relative_to(DOCS_DIR))] = hash_file(path)
    return data

def main():
    print(f"{BLUE}=== Documentation Drift Diff ==={RESET}")

    SNAPSHOT_DIR.mkdir(exist_ok=True)

    current = snapshot_docs()

    if SNAPSHOT_FILE.exists():
        with SNAPSHOT_FILE.open() as f:
            previous = json.load(f)
    else:
        previous = {}

    added = sorted(set(current.keys()) - set(previous.keys()))
    removed = sorted(set(previous.keys()) - set(current.keys()))
    changed = sorted(
        f for f in current.keys() & previous.keys()
        if current[f] != previous[f]
    )

    if added:
        print(f"{GREEN}Added:{RESET}")
        for f in added:
            print(f"  + {f}")

    if removed:
        print(f"{RED}Removed:{RESET}")
        for f in removed:
            print(f"  - {f}")

    if changed:
        print(f"{YELLOW}Modified:{RESET}")
        for f in changed:
            print(f"  * {f}")

    # Save new snapshot
    with SNAPSHOT_FILE.open("w") as f:
        json.dump(current, f, indent=2)

    print(f"{GREEN}Snapshot updated.{RESET}")

if __name__ == "__main__":
    main()
