#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_NAME = "ssrf_console"
PACKAGE_ROOT = SRC_ROOT / PACKAGE_NAME

# External modules that should NEVER be rewritten
EXTERNAL_MODULES = {
    "fastapi",
    "passlib",
    "uvicorn",
    "pydantic",
    "jinja2",
    "httpx",
    "starlette",
    "rich",
    "asyncio",
    "typing",
    "json",
    "os",
    "sys",
    "pathlib",
}

# Regex patterns
IMPORT_RE = re.compile(r"^(from|import)\s+([a-zA-Z0-9_\.]+)")
DOUBLE_DOT_RE = re.compile(r"ssrf_console\.\.")

def ensure_sys_path():
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))


def rewrite_import(line: str):
    """Fix import paths while avoiding external modules."""
    stripped = line.strip()
    match = IMPORT_RE.match(stripped)
    if not match:
        return line

    keyword, module = match.groups()
    root = module.split(".")[0]

    # Skip external modules
    if root in EXTERNAL_MODULES:
        return line

    # Skip already-correct imports
    if module.startswith(PACKAGE_NAME):
        return line

    # Skip stdlib or unknown modules
    if "." not in module and module not in os.listdir(PACKAGE_ROOT):
        return line

    # Rewrite import
    new_module = f"{PACKAGE_NAME}.{module}"
    return line.replace(module, new_module, 1)


def fix_double_dots(line: str):
    """Fix accidental ssrf_console..module imports."""
    if "ssrf_console.." in line:
        return line.replace("ssrf_console..", "ssrf_console.")
    return line


def process_file(path: Path):
    """Apply all fixes to a single file."""
    lines = path.read_text().splitlines()
    new_lines = []

    for line in lines:
        line = fix_double_dots(line)
        line = rewrite_import(line)
        new_lines.append(line)

    path.write_text("\n".join(new_lines))


def find_missing_internal_modules():
    """Detect imports pointing to modules that do not exist."""
    missing = []

    for py_file in PACKAGE_ROOT.rglob("*.py"):
        text = py_file.read_text().splitlines()

        for line in text:
            match = IMPORT_RE.match(line.strip())
            if not match:
                continue

            _, module = match.groups()

            # Only check internal modules
            if not module.startswith(PACKAGE_NAME):
                continue

            rel_path = module.replace(".", "/") + ".py"
            abs_path = SRC_ROOT / rel_path

            if not abs_path.exists():
                missing.append((py_file, module, abs_path))

    return missing


def main():
    ensure_sys_path()

    print("\n=== Repairing Imports ===\n")

    # Step 1: Fix imports in all files
    for py_file in PACKAGE_ROOT.rglob("*.py"):
        print(f"[FIX] {py_file}")
        process_file(py_file)

    # Step 2: Detect missing internal modules
    print("\n=== Checking for Missing Internal Modules ===\n")
    missing = find_missing_internal_modules()

    if not missing:
        print("[OK] No missing internal modules detected.")
    else:
        print(f"[!] {len(missing)} missing modules detected:\n")
        for src_file, module, expected_path in missing:
            print(f"Source: {src_file}")
            print(f"Import: {module}")
            print(f"Missing file: {expected_path}")
            print("")

    print("\n=== Import Repair Complete ===\n")


if __name__ == "__main__":
    main()
