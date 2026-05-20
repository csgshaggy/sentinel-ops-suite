#!/usr/bin/env python3
import json
from pathlib import Path

BLUE = "\033[34m"
GREEN = "\033[32m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
MAP_FILE = DOCS_DIR / "category_map.json"
OUTPUT = DOCS_DIR / "index" / "DOCS_INDEX.md"


def main():
    print(f"{BLUE}=== Generating Documentation Index ==={RESET}")

    with MAP_FILE.open() as f:
        category_map = json.load(f)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w") as out:
        out.write("# Documentation Index\n\n")

        for category, files in category_map.items():
            out.write(f"## {category.capitalize()}\n\n")
            for f in files:
                out.write(f"- [{f}](/docs/{category}/{f})\n")
            out.write("\n")

    print(f"{GREEN}Index generated at {OUTPUT}{RESET}")


if __name__ == "__main__":
    main()
