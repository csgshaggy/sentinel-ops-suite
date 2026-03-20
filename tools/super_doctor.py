import os
import ast
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

PROJECT_ROOT = Path.home() / "ssrf-command-console"
SRC_ROOT = PROJECT_ROOT / "src"

RUNTIME_DIR = PROJECT_ROOT / "runtime"
HISTORY_DIR = RUNTIME_DIR / "history"
LOG_PATH = RUNTIME_DIR / "super_doctor_report.json"

results = []

def log(severity, message):
    print(f"[{severity}] {message}")
    results.append({"severity": severity, "message": message})

def ensure_dirs():
    RUNTIME_DIR.mkdir(exist_ok=True)
    HISTORY_DIR.mkdir(exist_ok=True)

def check_missing_init():
    log("INFO", "Checking for missing __init__.py files...")
    missing = []

    for root, dirs, files in os.walk(SRC_ROOT):
        if any(f.endswith(".py") for f in files):
            if "__init__.py" not in files:
                missing.append(Path(root))

    if not missing:
        log("INFO", "No missing __init__.py files.")
    else:
        for p in missing:
            log("WARN", f"Missing __init__.py in: {p}")

def collect_import_graph():
    graph = defaultdict(set)
    all_files = []

    for py_file in SRC_ROOT.rglob("*.py"):
        all_files.append(py_file)
        try:
            tree = ast.parse(py_file.read_text(), filename=str(py_file))
        except Exception:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    graph[str(py_file)].add(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    graph[str(py_file)].add(node.module)

    return graph, all_files

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
            log("WARN", "Circular import: " + " -> ".join(cycle))

def write_json_report():
    ensure_dirs()

    with LOG_PATH.open("w") as f:
        json.dump(results, f, indent=2)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    history_path = HISTORY_DIR / f"super_doctor_{ts}.json"
    with history_path.open("w") as f:
        json.dump(results, f, indent=2)

    print(f"\nJSON report written to: {LOG_PATH}")
    print(f"History snapshot written to: {history_path}")

def main():
    print("=== Super Doctor ===")
    print(f"Project root: {PROJECT_ROOT}")

    check_missing_init()
    graph, files = collect_import_graph()
    check_circular_imports(graph)

    write_json_report()
    print("=== Super Doctor Complete ===")

if __name__ == "__main__":
    main()
