#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import ast

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_NAME = "ssrf_console"
PACKAGE_ROOT = SRC_ROOT / PACKAGE_NAME


def ensure_sys_path():
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))


def parse_internal_imports(py_file: Path):
    """Return internal imports from a Python file."""
    internal = []
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
    except Exception:
        return internal

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith(PACKAGE_NAME):
                internal.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(PACKAGE_NAME):
                    internal.append(alias.name)

    return internal


def module_to_path(module: str) -> Path:
    """Convert module path to filesystem path."""
    rel = module.replace(".", "/") + ".py"
    return SRC_ROOT / rel


def detect_missing_modules():
    """Return list of (source_file, module_name, expected_path)."""
    missing = []
    for py_file in PACKAGE_ROOT.rglob("*.py"):
        imports = parse_internal_imports(py_file)
        for mod in imports:
            expected = module_to_path(mod)
            if not expected.exists():
                missing.append((py_file, mod, expected))
    return sorted(set(missing))


def create_stub(path: Path):
    """Create a missing module stub."""
    print(f"[CREATE] {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Auto-generated stub module\n"
        "# This file was created by auto_fix_missing_modules.py\n\n"
        "def placeholder():\n"
        "    return 'stub'\n"
    )


def main():
    ensure_sys_path()

    print("\n=== Auto-Fix Missing Internal Modules ===\n")

    missing = detect_missing_modules()

    if not missing:
        print("[OK] No missing modules detected.")
        return

    print(f"[!] {len(missing)} missing modules detected.\n")

    for src, mod, expected in missing:
        print(f"Source: {src}")
        print(f"Missing module: {mod}")
        print(f"Expected path: {expected}")
        create_stub(expected)
        print("")

    print("\n=== Auto-Fix Complete ===\n")


if __name__ == "__main__":
    main()
