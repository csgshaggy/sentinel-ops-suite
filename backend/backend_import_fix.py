#!/usr/bin/env python3
import os
import re
import shutil

BACKEND_ROOT = "/home/ubuntu/sentinel-ops-suite/backend"

# Patterns to fix
REPLACEMENTS = {
    r"from backend\.app\.": "from app.",
    r"import backend\.app\.": "import app.",
    r"from backend\.src\.session_models": "from src.session_models",
    r"import backend\.src\.session_models": "import src.session_models",
}

def fix_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
    except UnicodeDecodeError:
        print(f"[SKIPPED - NON UTF8] {path}")
        return False

    updated = original
    for bad, good in REPLACEMENTS.items():
        updated = re.sub(bad, good, updated)

    if updated != original:
        backup = path + ".bak"
        shutil.copy2(path, backup)
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"[FIXED] {path}  (backup: {backup})")
        return True

    return False


def walk_and_fix():
    print("Scanning for invalid backend imports...\n")
    changed = 0

    for root, dirs, files in os.walk(BACKEND_ROOT):
        for file in files:
            if not file.endswith(".py"):
                continue

            full_path = os.path.join(root, file)
            if fix_file(full_path):
                changed += 1

    print("\nDone.")
    print(f"Total files modified: {changed}")


if __name__ == "__main__":
    walk_and_fix()
