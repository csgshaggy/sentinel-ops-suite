#!/usr/bin/env python3
import json
from pathlib import Path

BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
MAP_FILE = DOCS_DIR / "category_map.json"


def load_map():
    if not MAP_FILE.exists():
        print(f"{RED}[ERROR]{RESET} Missing category_map.json at {MAP_FILE}")
        raise SystemExit(1)
    with MAP_FILE.open() as f:
        return json.load(f)


def compute_health(category_map):
    score = 100
    deductions = 0

    # Missing dirs
    for cat in category_map.keys():
        if not (DOCS_DIR / cat).exists():
            deductions += 10

    # Missing mapped files
    for cat, files in category_map.items():
        for f in files:
            if not (DOCS_DIR / cat / f).exists():
                deductions += 5

    # Unmapped files
    mapped = {f for files in category_map.values() for f in files}
    unmapped = []
    for path in DOCS_DIR.rglob("*.md"):
        if path.name not in mapped:
            unmapped.append(path)
            deductions += 2

    score = max(0, score - deductions)
    return score, unmapped


def main():
    print(f"{BLUE}{BOLD}=== Documentation Dashboard ==={RESET}")

    category_map = load_map()
    categories = list(category_map.keys())

    mapped_files = [f for files in category_map.values() for f in files]
    mapped_count = len(mapped_files)

    all_md_files = list(DOCS_DIR.rglob("*.md"))
    all_md_count = len(all_md_files)

    health_score, unmapped = compute_health(category_map)

    print("")
    print(f"{BOLD}Categories:{RESET}       {len(categories)}")
    print(f"{BOLD}Mapped files:{RESET}    {mapped_count}")
    print(f"{BOLD}.md files on disk:{RESET} {all_md_count}")
    print("")

    color = GREEN if health_score >= 80 else (YELLOW if health_score >= 60 else RED)
    print(f"{BOLD}Health score:{RESET} {color}{health_score}/100{RESET}")
    print("")

    if unmapped:
        print(f"{YELLOW}Unmapped files:{RESET}")
        for path in unmapped:
            print(f"  - {path.relative_to(DOCS_DIR)}")
    else:
        print(f"{GREEN}No unmapped files.{RESET}")


if __name__ == "__main__":
    main()
