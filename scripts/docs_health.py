#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
MAP_FILE = DOCS_DIR / "category_map.json"

def fail(msg):
    print(f"{RED}[ERROR]{RESET} {msg}")
    sys.exit(1)

def load_map():
    if not MAP_FILE.exists():
        fail(f"Missing category_map.json at {MAP_FILE}")
    with MAP_FILE.open() as f:
        return json.load(f)

def main():
    print(f"{BLUE}=== Documentation Health Check ==={RESET}")

    category_map = load_map()
    categories = list(category_map.keys())

    score = 100
    deductions = []

    # 1. Check directories
    for cat in categories:
        if not (DOCS_DIR / cat).exists():
            deductions.append((10, f"Missing directory: {cat}/"))

    # 2. Check mapped files
    for cat, files in category_map.items():
        for f in files:
            expected = DOCS_DIR / cat / f
            if not expected.exists():
                deductions.append((5, f"Missing file: {cat}/{f}"))

    # 3. Check misplaced files
    for cat, files in category_map.items():
        for f in files:
            expected = DOCS_DIR / cat / f
            for path in DOCS_DIR.rglob(f):
                if path != expected:
                    deductions.append((5, f"Misplaced file: {path} (expected {expected})"))

    # 4. Unmapped files
    mapped = {f for files in category_map.values() for f in files}
    for path in DOCS_DIR.rglob("*.md"):
        if path.name not in mapped:
            deductions.append((2, f"Unmapped file: {path}"))

    # Apply deductions
    for d, msg in deductions:
        print(f"{YELLOW}[WARN]{RESET} {msg}")
        score -= d

    score = max(score, 0)

    print("")
    print(f"{BLUE}Documentation Health Score: {GREEN}{score}/100{RESET}")

    if score < 70:
        print(f"{RED}Documentation health is below acceptable threshold.{RESET}")
        sys.exit(1)

    print(f"{GREEN}Documentation health OK.{RESET}")

if __name__ == "__main__":
    main()
