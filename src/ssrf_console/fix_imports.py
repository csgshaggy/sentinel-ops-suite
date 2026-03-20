#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path("src/ssrf_console")

# Regex to match "from X import Y" or "import X"
IMPORT_RE = re.compile(r"^(from|import)\s+([a-zA-Z0-9_\.]+)")

def rewrite_import(line: str):
    match = IMPORT_RE.match(line.strip())
    if not match:
        return line

    keyword, module = match.groups()

    # Skip already-correct imports
    if module.startswith("ssrf_console"):
        return line

    # Skip stdlib or external imports
    if "." not in module and module not in os.listdir(ROOT):
        return line

    # Rewrite
    new_module = f"ssrf_console.{module}"
    return line.replace(module, new_module, 1)

def process_file(path: Path):
    text = path.read_text().splitlines()
    new_lines = [rewrite_import(line) for line in text]
    path.write_text("\n".join(new_lines))

def main():
    for py_file in ROOT.rglob("*.py"):
        print(f"[FIX] {py_file}")
        process_file(py_file)

if __name__ == "__main__":
    main()
