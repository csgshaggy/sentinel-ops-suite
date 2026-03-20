import os
import ast
import json
import importlib
import pkgutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

PROJECT_ROOT = Path.home() / "ssrf-command-console"
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "ssrf_console"

RUNTIME_DIR = PROJECT_ROOT / "runtime"
HISTORY_DIR = RUNTIME_DIR / "history"
LOG_PATH = RUNTIME_DIR / "super_doctor_report.json"

SEVERITY = {
    "INFO": 1,
    "WARN": 2,
    "FAIL": 3,
}

results = []


def log(severity, message):
    print(f"[{severity}] {message}")
    results.append({"severity": severity, "message": message})


def ensure_runtime_dirs():
    RUNTIME_DIR.mkdir(exist_ok=True)
    HISTORY_DIR.mkdir(exist_ok=True)


def check_missing_init():
    log("INFO", "Checking for missing __init__.py files...")
    missing = []

    for root, dirs, files in os.walk(PACKAGE_ROOT):
        py_files = [f for f in files if f.endswith(".py")]
        if py_files and "__init__.py" not in files:
            missing.append(Path(root))

    if not missing:
        log("INFO", "No missing __init__.py files.")
    else:
        for p in missing:
            log("FAIL", f"Missing __init__.py in: {p}")


def collect_import_graph():
    graph = defaultdict(set)
    all_modules = set()

    for module in pkgutil.walk_packages([str(PACKAGE_ROOT)], "ssrf_console."):
        name = module.name
        all_modules.add(name)

        try:
            spec = importlib.util.find_spec(name)
            if not spec or not spec.origin or not spec.origin.endswith(".py"):
                continue

            path = Path(spec.origin)
            with path.open("r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith("ssrf_console."):
                            graph[name].add(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module.startswith("ssrf_console."):
                        graph[name].add(node.module)

        except Exception as e:
            log("WARN", f"Failed to parse {name}: {e}")

    return graph, all_modules


def check_circular_imports(graph):
    log("INFO", "Checking for circular imports...")
    visited = set()
    stack = []
    cycles = []

    def dfs(node):
        if node in stack:
            cycle = stack[stack.index(node):] + [node]
            cycles.append(cycle)
            return
        if node in visited:
            return

        visited.add(node)
        stack.append(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor)
        stack.pop()

    for node in graph.keys():
        dfs(node)

    if not cycles:
        log("INFO", "No circular imports detected.")
    else:
        for cycle in cycles:
            log("FAIL", "Circular import: " + " -> ".join(cycle))


def check_orphaned_and_dead_files(all_modules):
    log("INFO", "Checking for orphaned and dead Python files...")

    module_to_file = {}
    for module in all_modules:
        try:
            spec = importlib.util.find_spec(module)
            if spec and spec.origin and spec.origin.endswith(".py"):
                module_to_file[module] = Path(spec.origin)
        except Exception:
            continue

    all_py_files = set()
    for root, dirs, files in os.walk(PACKAGE_ROOT):
        for f in files:
            if f.endswith(".py"):
                all_py_files.add(Path(root) / f)

    importable_files = set(module_to_file.values())
    orphaned_files = all_py_files - importable_files

    if not orphaned_files:
        log("INFO", "No orphaned Python files.")
    else:
        for p in sorted(orphaned_files):
            log("WARN", f"Orphaned Python file: {p}")


def write_json_report():
    ensure_runtime_dirs()

    # latest report
    with LOG_PATH.open("w") as f:
        json.dump(results, f, indent=2)

    # timestamped history snapshot
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    history_path = HISTORY_DIR / f"super_doctor_{ts}.json"
    with history_path.open("w") as f:
        json.dump(results, f, indent=2)

    print(f"\nJSON report written to: {LOG_PATH}")
    print(f"History snapshot written to: {history_path}")


def main():
    print("=== Super Doctor (Enhanced) ===")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Package root: {PACKAGE_ROOT}")

    if not PACKAGE_ROOT.exists():
        log("FAIL", f"Package root not found: {PACKAGE_ROOT}")
        write_json_report()
        return

    check_missing_init()
    graph, all_modules = collect_import_graph()
    check_circular_imports(graph)
    check_orphaned_and_dead_files(all_modules)

    write_json_report()
    print("=== Super Doctor Complete ===")


if __name__ == "__main__":
    main()
