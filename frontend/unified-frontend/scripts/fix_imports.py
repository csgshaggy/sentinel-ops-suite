#!/usr/bin/env python3
import os
import re
from pathlib import Path

SRC_DIR = Path("src")

IMPORT_RE = re.compile(r'from\s+["\'](.+?)["\']')

def find_file(filename):
    """Search for a file anywhere under src/."""
    matches = []
    for root, dirs, files in os.walk(SRC_DIR):
        if filename in files:
            matches.append(Path(root) / filename)
    return matches

def compute_relative(from_file, to_file):
    return os.path.relpath(to_file, start=from_file.parent)

def process_file(path):
    text = path.read_text()
    changed = False
    new_lines = []

    for line in text.splitlines():
        m = IMPORT_RE.search(line)
        if not m:
            new_lines.append(line)
            continue

        import_path = m.group(1)

        # Skip absolute, node_modules, or external imports
        if not import_path.startswith("."):
            new_lines.append(line)
            continue

        # Resolve the referenced file
        target = (path.parent / import_path).resolve()

        if target.exists():
            new_lines.append(line)
            continue

        # Try to find the correct file by filename
        filename = Path(import_path).name
        matches = find_file(filename)

        if not matches:
            print(f"[WARN] No match found for {filename} (from {path})")
            new_lines.append(line)
            continue

        # Pick the first match (usually correct)
        correct = matches[0]
        rel = compute_relative(path, correct)

        new_line = line.replace(import_path, rel)
        print(f"[FIX] {path} → {import_path} -> {rel}")
        new_lines.append(new_line)
        changed = True

    if changed:
        path.write_text("\n".join(new_lines))

def main():
    print("[IMPORT-FIX] Scanning for broken imports...")
    for root, dirs, files in os.walk(SRC_DIR):
        for f in files:
            if f.endswith(".jsx") or f.endswith(".js"):
                process_file(Path(root) / f)
    print("[IMPORT-FIX] Done.")

if __name__ == "__main__":
    main()
