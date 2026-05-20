#!/usr/bin/env python3
"""
SentinelOps Backend Code Health Tool
------------------------------------
Features:
- Detect & auto-fix invalid imports (with backups)
- Detect unused imports
- Detect likely circular imports (import graph)
- Emit JSON report (issues + fixes)
- CI / pre-commit friendly (non-zero exit if issues remain)

Usage:
    python code_health.py          # scan + autofix invalid imports
    python code_health.py --report # scan only, JSON report, no fixes
"""

import ast
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[0]

SCAN_ROOTS = [
    PROJECT_ROOT / "app",
    PROJECT_ROOT / "src",
    PROJECT_ROOT / "routes",
    PROJECT_ROOT / "auth",
]

# Known rewrites tailored to your project
REWRITE_MAP = {
    "app.models.users": "app.models.user",
    "app.db.users": "app.repositories.user_repository",
    "app.core.session": "src.session_models",
    "backend.app": "app",
    "backend.src": "src",
    "backend.routes": "app.routers",
}

@dataclass
class ImportIssue:
    file: str
    line: int
    col: int
    import_type: str  # "import" or "from"
    module: str
    name: Optional[str]
    action: str       # "rewrite", "comment", "unused", "circular"
    detail: str

@dataclass
class FileReport:
    path: str
    invalid_imports: List[ImportIssue]
    unused_imports: List[ImportIssue]


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


def discover_python_files() -> List[Path]:
    files: List[Path] = []
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for f in root.rglob("*.py"):
            files.append(f)
    return files


def parse_ast(path: Path) -> Optional[ast.AST]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        print(f"[SKIP] Non-UTF8 or unreadable: {path}")
        return None
    try:
        return ast.parse(text)
    except SyntaxError:
        print(f"[SKIP] Syntax error: {path}")
        return None


def build_import_graph(files: List[Path]) -> Dict[str, Set[str]]:
    """
    Build a simple import graph: module_name -> set(imported_module_names)
    Used for circular import detection.
    """
    graph: Dict[str, Set[str]] = defaultdict(set)

    def module_name_from_path(p: Path) -> str:
        rel = p.relative_to(PROJECT_ROOT)
        parts = list(rel.with_suffix("").parts)
        return ".".join(parts)

    for path in files:
        tree = parse_ast(path)
        if not tree:
            continue
        this_mod = module_name_from_path(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    graph[this_mod].add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                graph[this_mod].add(node.module)
    return graph


def detect_circular_imports(graph: Dict[str, Set[str]]) -> List[Tuple[str, str]]:
    """
    Very simple cycle detection: looks for A->B and B->A.
    Not a full graph cycle detector, but enough to flag obvious problems.
    """
    cycles: List[Tuple[str, str]] = []
    for a, targets in graph.items():
        for b in targets:
            if b in graph and a in graph[b]:
                pair = tuple(sorted((a, b)))
                if pair not in cycles:
                    cycles.append(pair)
    return cycles


def analyze_file_for_imports(path: Path) -> Tuple[List[ImportIssue], List[ImportIssue]]:
    """
    Returns (invalid_imports, unused_imports) for a file.
    """
    invalid: List[ImportIssue] = []
    unused: List[ImportIssue] = []

    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return invalid, unused

    tree = parse_ast(path)
    if not tree:
        return invalid, unused

    # Track imports and usage
    imported_names: Dict[Tuple[str, Optional[str]], ast.AST] = {}
    used_names: Set[str] = set()

    class UsageVisitor(ast.NodeVisitor):
        def visit_Name(self, node: ast.Name):
            used_names.add(node.id)

    UsageVisitor().visit(tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name
                imported_names[(module, None)] = node
                if not module_exists(module):
                    invalid.append(
                        ImportIssue(
                            file=str(path),
                            line=node.lineno,
                            col=node.col_offset,
                            import_type="import",
                            module=module,
                            name=None,
                            action="invalid",
                            detail="Module does not exist",
                        )
                    )
        elif isinstance(node, ast.ImportFrom):
            if not node.module:
                continue
            module = node.module
            for alias in node.names:
                imported_names[(module, alias.name)] = node
            if not module_exists(module):
                invalid.append(
                    ImportIssue(
                        file=str(path),
                        line=node.lineno,
                        col=node.col_offset,
                        import_type="from",
                        module=module,
                        name=None,
                        action="invalid",
                        detail="Module does not exist",
                    )
                )

    # Detect unused imports (only for modules that actually exist)
    for (module, name), node in imported_names.items():
        if name is None:
            # "import module"
            base = module.split(".")[0]
            if base not in used_names and module_exists(module):
                unused.append(
                    ImportIssue(
                        file=str(path),
                        line=node.lineno,
                        col=node.col_offset,
                        import_type="import",
                        module=module,
                        name=None,
                        action="unused",
                        detail="Imported but never used",
                    )
                )
        else:
            # "from module import name"
            if name not in used_names and module_exists(module):
                unused.append(
                    ImportIssue(
                        file=str(path),
                        line=node.lineno,
                        col=node.col_offset,
                        import_type="from",
                        module=module,
                        name=name,
                        action="unused",
                        detail="Imported but never used",
                    )
                )

    return invalid, unused


def apply_fixes(path: Path, invalid_imports: List[ImportIssue]) -> None:
    """
    Auto-fix invalid imports in a file:
    - If REWRITE_MAP has a mapping → rewrite
    - Else → comment out the import line
    """
    if not invalid_imports:
        return

    try:
        original = path.read_text(encoding="utf-8")
    except Exception:
        print(f"[SKIP] Cannot read for fix: {path}")
        return

    lines = original.splitlines()
    modified = False

    for issue in invalid_imports:
        module = issue.module
        new_module = REWRITE_MAP.get(module)

        if issue.import_type == "import":
            if new_module:
                print(f"[REWRITE] {module} → {new_module} in {path}")
                pattern = rf"\bimport\s+{re.escape(module)}\b"
                repl = f"import {new_module}"
                lines = [re.sub(pattern, repl, line) for line in lines]
                modified = True
            else:
                print(f"[COMMENT] Invalid import {module} in {path}")
                pattern = rf"\bimport\s+{re.escape(module)}\b"
                lines = [
                    re.sub(
                        pattern,
                        f"# INVALID IMPORT REMOVED: {module}",
                        line,
                    )
                    for line in lines
                ]
                modified = True

        elif issue.import_type == "from":
            if new_module:
                print(f"[REWRITE] {module} → {new_module} in {path}")
                pattern = rf"\bfrom\s+{re.escape(module)}\s+import\b"
                repl = f"from {new_module} import"
                lines = [re.sub(pattern, repl, line) for line in lines]
                modified = True
            else:
                print(f"[COMMENT] Invalid import {module} in {path}")
                pattern = rf"\bfrom\s+{re.escape(module)}\s+import\b"
                lines = [
                    re.sub(
                        pattern,
                        f"# INVALID IMPORT REMOVED: {module}",
                        line,
                    )
                    for line in lines
                ]
                modified = True

    if modified:
        backup = path.with_suffix(path.suffix + ".bak")
        backup.write_text(original, encoding="utf-8")
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"[FIXED] {path} (backup → {backup})")


def main():
    report_only = "--report" in sys.argv

    files = discover_python_files()
    graph = build_import_graph(files)
    cycles = detect_circular_imports(graph)

    file_reports: List[FileReport] = []
    any_invalid = False
    any_unused = False

    for path in files:
        invalid, unused = analyze_file_for_imports(path)
        if invalid or unused:
            file_reports.append(
                FileReport(
                    path=str(path),
                    invalid_imports=invalid,
                    unused_imports=unused,
                )
            )
        if invalid:
            any_invalid = True
        if unused:
            any_unused = True

        if invalid and not report_only:
            apply_fixes(path, invalid)

    # Build JSON report
    json_report = {
        "files": [
            {
                "path": fr.path,
                "invalid_imports": [asdict(i) for i in fr.invalid_imports],
                "unused_imports": [asdict(i) for i in fr.unused_imports],
            }
            for fr in file_reports
        ],
        "circular_imports": [
            {"module_a": a, "module_b": b} for (a, b) in cycles
        ],
    }

    report_path = PROJECT_ROOT / "code_health_report.json"
    report_path.write_text(json.dumps(json_report, indent=2), encoding="utf-8")
    print(f"\n[REPORT] Written to {report_path}")

    if cycles:
        print("\n[WARN] Circular import pairs detected:")
        for a, b in cycles:
            print(f"  - {a} <-> {b}")

    if any_invalid or any_unused or cycles:
        print("\n[STATUS] Issues detected.")
        # Non-zero exit for CI / pre-commit
        sys.exit(1)
    else:
        print("\n[STATUS] Clean build. No import issues detected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
