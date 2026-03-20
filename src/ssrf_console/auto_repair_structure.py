#!/usr/bin/env python3
import os
import sys
import ast
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_NAME = "ssrf_console"
PACKAGE_ROOT = SRC_ROOT / PACKAGE_NAME


def ensure_sys_path():
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))


def find_internal_imports(py_file: Path):
    """Parse imports inside a Python file and return internal module paths."""
    internal = []
    tree = ast.parse(py_file.read_text())

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith(PACKAGE_NAME):
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


def create_missing_stub(path: Path):
    """Create a missing module stub."""
    print(f"[CREATE] Missing module stub: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Auto-created stub module\n")


def find_misplaced_modules():
    """Find Python files that belong inside ssrf_console but are outside."""
    misplaced = []
    for py_file in PROJECT_ROOT.rglob("*.py"):
        if "src/ssrf_console" in str(py_file):
            continue
        if py_file.name in ("auto_repair_structure.py", "fix_imports.py", "validate_imports.py"):
            continue
        # Heuristic: if file imports ssrf_console.*, it belongs inside the package
        text = py_file.read_text()
        if "ssrf_console." in text:
            misplaced.append(py_file)
    return misplaced


def move_misplaced_module(py_file: Path):
    """Move a misplaced module into the correct package folder."""
    print(f"[MOVE] Misplaced module: {py_file}")
    dest = PACKAGE_ROOT / py_file.name
    shutil.move(str(py_file), str(dest))


def detect_circular_imports():
    """Detect circular imports by building a dependency graph."""
    print("\n=== Checking for Circular Imports ===\n")

    graph = {}
    for py_file in PACKAGE_ROOT.rglob("*.py"):
        module_name = (
            str(py_file.relative_to(SRC_ROOT))
            .replace("/", ".")
            .replace(".py", "")
        )
        imports = find_internal_imports(py_file)
        graph[module_name] = imports

    circular = []

    def visit(node, stack):
        if node in stack:
            circular.append(stack + [node])
            return
        for dep in graph.get(node, []):
            visit(dep, stack + [node])

    for module in graph:
        visit(module, [])

    if not circular:
        print("[OK] No circular imports detected.")
    else:
        print(f"[!] {len(circular)} circular import chains found:\n")
        for chain in circular:
            print(" -> ".join(chain))


def main():
    ensure_sys_path()

    print("\n=== Auto Repair: Missing Modules, Misplaced Files, Circular Imports ===\n")

    # Step 1 — Detect missing internal modules
    print("[*] Scanning for missing internal modules...\n")
    missing = []

    for py_file in PACKAGE_ROOT.rglob("*.py"):
        internal_imports = find_internal_imports(py_file)
        for module in internal_imports:
            expected_path = module_to_path(module)
            if not expected_path.exists():
                missing.append(expected_path)

    missing = sorted(set(missing))

    if missing:
        print(f"[!] {len(missing)} missing modules detected.\n")
        for path in missing:
            create_missing_stub(path)
    else:
        print("[OK] No missing modules.\n")

    # Step 2 — Detect and move misplaced modules
    print("[*] Scanning for misplaced modules...\n")
    misplaced = find_misplaced_modules()

    if misplaced:
        print(f"[!] {len(misplaced)} misplaced modules found.\n")
        for py_file in misplaced:
            move_misplaced_module(py_file)
    else:
        print("[OK] No misplaced modules.\n")

    # Step 3 — Detect circular imports
    detect_circular_imports()

    print("\n=== Auto Repair Complete ===\n")


if __name__ == "__main__":
    main()
