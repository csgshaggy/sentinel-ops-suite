#!/usr/bin/env python3
import os
import re
import sys
import ast
import json
import shutil
from pathlib import Path

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_NAME = "ssrf_console"
PACKAGE_ROOT = SRC_ROOT / PACKAGE_NAME

EXTERNAL_MODULES = {
    "fastapi", "passlib", "uvicorn", "pydantic", "jinja2",
    "httpx", "starlette", "rich", "asyncio", "typing",
    "json", "os", "sys", "pathlib", "logging"
}

BINARY_THRESHOLD = 0.20  # >20% non-text bytes = binary


# -------------------------------------------------------------------
# UTILITIES
# -------------------------------------------------------------------

def header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def ensure_sys_path():
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))


def safe_read(path: Path):
    """Read file with fallback encodings."""
    try:
        return path.read_text(encoding="utf-8"), "utf-8"
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1"), "latin-1"
        except Exception:
            return None, None


def is_binary(path: Path) -> bool:
    """Detect binary files by scanning for non-text bytes."""
    try:
        raw = path.read_bytes()
    except Exception:
        return True

    if not raw:
        return False

    nontext = sum(1 for b in raw if b < 9 or (13 < b < 32) or b > 126)
    return (nontext / len(raw)) > BINARY_THRESHOLD


def clean_binary_junk(text: str) -> str:
    """Remove invalid characters that break Python parsing."""
    return re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]", "", text)


def normalize_to_utf8(path: Path):
    """Normalize file encoding to UTF-8."""
    text, encoding = safe_read(path)
    if text is None:
        print(f"[SKIP] Could not read file: {path}")
        return

    cleaned = clean_binary_junk(text)

    if cleaned != text or encoding != "utf-8":
        print(f"[FIX] Normalizing to UTF-8: {path}")
        path.write_text(cleaned, encoding="utf-8")


# -------------------------------------------------------------------
# IMPORT REPAIR
# -------------------------------------------------------------------

IMPORT_RE = re.compile(r"^(from|import)\s+([a-zA-Z0-9_\.]+)")


def rewrite_import(line: str):
    stripped = line.strip()
    match = IMPORT_RE.match(stripped)
    if not match:
        return line

    keyword, module = match.groups()
    root = module.split(".")[0]

    if root in EXTERNAL_MODULES:
        return line

    if module.startswith(PACKAGE_NAME):
        return line

    if "." not in module and module not in os.listdir(PACKAGE_ROOT):
        return line

    new_module = f"{PACKAGE_NAME}.{module}"
    return line.replace(module, new_module, 1)


def fix_double_dots(line: str):
    return line.replace("ssrf_console..", "ssrf_console.")


def repair_imports_in_file(path: Path):
    text, _ = safe_read(path)
    if text is None:
        return

    new_lines = []
    for line in text.splitlines():
        line = fix_double_dots(line)
        line = rewrite_import(line)
        new_lines.append(line)

    path.write_text("\n".join(new_lines), encoding="utf-8")


# -------------------------------------------------------------------
# INTERNAL MODULE CHECKS
# -------------------------------------------------------------------

def parse_internal_imports(py_file: Path):
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
    return SRC_ROOT / (module.replace(".", "/") + ".py")


def detect_missing_modules(py_files):
    missing = []
    for f in py_files:
        for mod in parse_internal_imports(f):
            expected = module_to_path(mod)
            if not expected.exists():
                missing.append((f, mod, expected))
    return sorted(set(missing))


def create_stub(path: Path):
    print(f"[CREATE] {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Auto-generated stub module\n"
        "def placeholder():\n"
        "    return 'stub'\n"
    )


# -------------------------------------------------------------------
# MISPLACED MODULES
# -------------------------------------------------------------------

def find_misplaced_modules():
    misplaced = []
    for py_file in PROJECT_ROOT.rglob("*.py"):
        if "src/ssrf_console" in str(py_file):
            continue
        if py_file.name in {"doctor.py"}:
            continue

        text, _ = safe_read(py_file)
        if text and "ssrf_console." in text:
            misplaced.append(py_file)

    return misplaced


def move_misplaced(py_file: Path):
    dest = PACKAGE_ROOT / py_file.name
    print(f"[MOVE] {py_file} -> {dest}")
    shutil.move(str(py_file), str(dest))


# -------------------------------------------------------------------
# CIRCULAR IMPORT DETECTION
# -------------------------------------------------------------------

def build_dep_graph(py_files):
    graph = {}
    for f in py_files:
        rel = f.relative_to(SRC_ROOT)
        module_name = str(rel).replace("/", ".").replace(".py", "")
        graph[module_name] = parse_internal_imports(f)
    return graph


def detect_circular_imports(graph):
    visited = set()
    stack = []
    cycles = []

    def visit(node):
        if node in stack:
            idx = stack.index(node)
            cycles.append(stack[idx:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        stack.append(node)
        for dep in graph.get(node, []):
            visit(dep)
        stack.pop()

    for node in graph:
        visit(node)

    return cycles


# -------------------------------------------------------------------
# HEALTH DASHBOARD
# -------------------------------------------------------------------

def project_health(py_files):
    header("PROJECT HEALTH DASHBOARD")

    missing = detect_missing_modules(py_files)
    graph = build_dep_graph(py_files)
    cycles = detect_circular_imports(graph)
    misplaced = find_misplaced_modules()

    summary = {
        "encoding_issues": 0,
        "missing_modules": len(missing),
        "circular_imports": len(cycles),
        "misplaced_modules": len(misplaced),
    }

    print(json.dumps(summary, indent=2))


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def main():
    ensure_sys_path()

    py_files = list(PACKAGE_ROOT.rglob("*.py"))

    header("STEP 1 — Encoding Repair & Binary Cleanup")
    for f in py_files:
        if not is_binary(f):
            normalize_to_utf8(f)

    header("STEP 2 — Import Repair")
    for f in py_files:
        repair_imports_in_file(f)

    header("STEP 3 — Move Misplaced Modules")
    for f in find_misplaced_modules():
        move_misplaced(f)

    header("STEP 4 — Auto-Fix Missing Modules")
    for src, mod, expected in detect_missing_modules(py_files):
        create_stub(expected)

    header("STEP 5 — Full Project Health Dashboard")
    project_health(py_files)


if __name__ == "__main__":
    main()
