#!/usr/bin/env python3
from pathlib import Path

# ------------------------------------------------------------
# Resolve project root and docs directory
# ------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DOCS_DIR = PROJECT_ROOT / "docs"
HELP_FILE = PROJECT_ROOT / "HELP.md"

if not DOCS_DIR.exists():
    raise SystemExit(f"ERROR: docs/ directory not found at {DOCS_DIR}")


# ------------------------------------------------------------
# Utility: natural sort for categories like 00, 10, 20...
# ------------------------------------------------------------
def natural_key(path: Path):
    name = path.name
    prefix = name.split("-")[0]
    return int(prefix) if prefix.isdigit() else 9999


# ------------------------------------------------------------
# Scan categories
# ------------------------------------------------------------
categories = sorted([p for p in DOCS_DIR.iterdir() if p.is_dir()], key=natural_key)

# Include testing directory last if present
testing_dir = DOCS_DIR / "testing"
if testing_dir.exists():
    categories.append(testing_dir)

# ------------------------------------------------------------
# Build HELP.md content
# ------------------------------------------------------------
lines = []
lines.append("# 📘 Project Documentation — Help & Table of Contents\n")
lines.append("This file is auto‑generated. Do not edit manually.\n")
lines.append("---\n")
lines.append("# 📑 Table of Contents\n")

for category in categories:
    cat_name = category.name

    # Pretty title: "10-overview" → "10 — Overview"
    if "-" in cat_name:
        prefix, label = cat_name.split("-", 1)
        title = f"{prefix} — {label.replace('_', ' ').title()}"
    else:
        title = cat_name.title()

    lines.append(f"\n## {title}")

    # List files inside category
    md_files = sorted(category.glob("*.md"))
    for f in md_files:
        display = f.stem.replace("_", " ").title()
        rel_path = f"docs/{category.name}/{f.name}"
        lines.append(f"- [{display}]({rel_path})")

# ------------------------------------------------------------
# Write HELP.md
# ------------------------------------------------------------
HELP_FILE.write_text("\n".join(lines), encoding="utf-8")

print(f"HELP.md generated at: {HELP_FILE}")
