#!/usr/bin/env python3
import json
from pathlib import Path
import re

BLUE = "\033[34m"
GREEN = "\033[32m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUT = PROJECT_ROOT / "docs_search_index.json"

HEADING_RE = re.compile(r"^(#+)\s+(.*)$")

def extract_metadata(md_text):
    lines = md_text.splitlines()

    title = None
    headings = []
    keywords = set()

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()

            if level == 1 and title is None:
                title = text

            headings.append(text)
            for word in text.split():
                keywords.add(word.lower())

    # fallback title
    if not title:
        title = "Untitled"

    return title, headings, sorted(keywords)

def main():
    print(f"{BLUE}=== Generating Documentation Search Index ==={RESET}")

    index = []

    for path in DOCS_DIR.rglob("*.md"):
        rel = path.relative_to(DOCS_DIR)
        md_text = path.read_text(encoding="utf-8")

        title, headings, keywords = extract_metadata(md_text)

        entry = {
            "file": str(rel),
            "title": title,
            "headings": headings,
            "keywords": keywords,
            "content": md_text,
        }

        index.append(entry)

    OUTPUT.write_text(json.dumps(index, indent=2), encoding="utf-8")

    print(f"{GREEN}Search index written to {OUTPUT}{RESET}")

if __name__ == "__main__":
    main()
