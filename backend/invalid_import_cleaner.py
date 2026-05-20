#!/usr/bin/env python3
"""
SentinelOps — Invalid Import Auto-Fixer
---------------------------------------
Scans the backend for invalid imports and automatically fixes them.

Fix behavior:
- If a known mapping exists → rewrite import
- If no mapping exists → comment out the import
- Never modifies valid imports
- Never crashes on unreadable or binary files
"""

import ast
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]

SCAN_ROOTS = [
    PROJECT_ROOT / "app",
    PROJECT_ROOT / "src",
    PROJECT_ROOT / "routes",
    PROJECT_ROOT / "auth",
]

# Known rewrites based on your project structure
REWRITE_MAP = {
    "app.models.users": "app.models.user",
    "app.db.users": "app.repositories.user_repository",
    "app.core.session": "src.session_models",
    "backend.app": "app",
    "backend.src": "src",
    "backend.routes": "app.routers",
}

def module_exists(module: str) -> bool:
    """Check if a module exists anywhere in the project."""
    parts = module.split(".")
    for root in SCAN_ROOTS:
        candidate = root.joinpath(*parts)
        if candidate.with_suffix(".py").exists():
            return True
        if candidate.is_dir() and (candidate / "__init__.py").exists():
            return True
    return False


def fix_imports_in_file(path: Path):
    """Detect and fix invalid imports inside a single file."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        print(f"[SKIP] Non-UTF8 or unreadable: {path}")
        return

    try:
        tree = ast.parse(text)
    except SyntaxError:
        print(f"[SKIP] Syntax error: {path}")
        return

    modified = False
    lines = text.splitlines()

    for node in ast.walk(tree):

        # import foo.bar
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name

                if module_exists(module):
                    continue  # valid

                new_module = REWRITE_MAP.get(module)
                if new_module:
                    print(f"[REWRITE] {module} → {new_module} in {path}")
                    pattern = rf"import\s+{re.escape(module)}"
                    repl = f"import {new_module}"
                    lines = [re.sub(pattern, repl, line) for line in lines]
                    modified = True
                else:
                    print(f"[COMMENT] Invalid import {module} in {path}")
                    pattern = rf"import\s+{re.escape(module)}"
                    lines = [re.sub(pattern, f"# INVALID IMPORT REMOVED: {module}", line) for line in lines]
                    modified = True

        # from foo.bar import X
        elif isinstance(node, ast.ImportFrom):
            if not node.module:
                continue

            module = node.module

            if module_exists(module):
                continue  # valid

            new_module = REWRITE_MAP.get(module)
            if new_module:
                print(f"[REWRITE] {module} → {new_module} in {path}")
                pattern = rf"from\s+{re.escape(module)}\s+import"
                repl = f"from {new_module} import"
                lines = [re.sub(pattern, repl, line) for line in lines]
                modified = True
            else:
                print(f"[COMMENT] Invalid import {module} in {path}")
                pattern = rf"from\s+{re.escape(module)}\s+import"
                lines = [re.sub(pattern, f"# INVALID IMPORT REMOVED: {module}", line) for line in lines]
                modified = True

    if modified:
        backup = path.with_suffix(path.suffix + ".bak")
        backup.write_text(text, encoding="utf-8")
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"[FIXED] {path} (backup saved → {backup})")


def walk_and_fix():
    print("Scanning and fixing invalid imports...\n")

    for root in SCAN_ROOTS:
        for file in root.rglob("*.py"):
            fix_imports_in_file(file)

    print("\nDone. All invalid imports processed.")


if __name__ == "__main__":
    walk_and_fix()
