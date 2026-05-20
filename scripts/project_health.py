#!/usr/bin/env python3
import ast
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_NAME = "ssrf_console"
PACKAGE_ROOT = SRC_ROOT / PACKAGE_NAME

RUNTIME_DIR = PROJECT_ROOT / "runtime"
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
TEMPLATES_DIR = PACKAGE_ROOT / "templates"
STATIC_DIR = PACKAGE_ROOT / "static"

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
    "logging",
}


def header(title: str):
    print("\n" + "=" * 80)
    print(f"{title}")
    print("=" * 80 + "\n")


def ensure_sys_path():
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))


def list_py_files(root: Path):
    return list(root.rglob("*.py"))


def check_encoding(py_files):
    issues = []
    for f in py_files:
        try:
            f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            issues.append(f)
    return issues


def parse_imports(py_file: Path):
    internal = []
    external = []
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
    except Exception:
        return internal, external

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                root = node.module.split(".")[0]
                if node.module.startswith(PACKAGE_NAME):
                    internal.append(node.module)
                elif root not in EXTERNAL_MODULES:
                    external.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if alias.name.startswith(PACKAGE_NAME):
                    internal.append(alias.name)
                elif root not in EXTERNAL_MODULES:
                    external.append(alias.name)
    return internal, external


def module_to_path(module: str) -> Path:
    rel = module.replace(".", "/") + ".py"
    return SRC_ROOT / rel


def check_missing_internal_modules(py_files):
    missing = []
    for f in py_files:
        internal, _ = parse_imports(f)
        for mod in internal:
            path = module_to_path(mod)
            if not path.exists():
                missing.append((f, mod, path))
    return sorted(set(missing))


def build_dep_graph(py_files):
    graph = {}
    for f in py_files:
        rel = f.relative_to(SRC_ROOT)
        module_name = str(rel).replace("/", ".").replace(".py", "")
        internal, _ = parse_imports(f)
        graph[module_name] = internal
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


def check_orphan_files(py_files):
    """Python files not under ssrf_console but inside src."""
    orphans = []
    for f in SRC_ROOT.rglob("*.py"):
        if PACKAGE_ROOT in f.parents:
            continue
        orphans.append(f)
    return orphans


def check_runtime_artifacts():
    artifacts = []
    if not RUNTIME_DIR.exists():
        return artifacts
    for p in RUNTIME_DIR.rglob("*"):
        if p.is_file():
            artifacts.append(p)
    return artifacts


def check_templates_and_static():
    missing = []
    if not TEMPLATES_DIR.exists():
        missing.append(("templates_dir_missing", TEMPLATES_DIR))
    if not STATIC_DIR.exists():
        missing.append(("static_dir_missing", STATIC_DIR))
    return missing


def check_config_files():
    issues = []
    if not CONFIG_DIR.exists():
        issues.append(("config_dir_missing", CONFIG_DIR))
        return issues

    expected = ["config.yaml", "ssrf_config.json"]
    for name in expected:
        p = CONFIG_DIR / name
        if not p.exists():
            issues.append(("missing_config", p))
    return issues


def check_requirements():
    req = PROJECT_ROOT / "requirements.txt"
    lock = PROJECT_ROOT / "requirements.lock"
    issues = []
    if not req.exists():
        issues.append("requirements.txt missing")
    if not lock.exists():
        issues.append("requirements.lock missing")
    return issues


def main():
    ensure_sys_path()

    header("PROJECT HEALTH DASHBOARD")

    # 1. Python files
    py_files = list_py_files(PACKAGE_ROOT)
    print(f"[INFO] Python files under package: {len(py_files)}")

    # 2. Encoding issues
    header("ENCODING CHECK")
    encoding_issues = check_encoding(py_files)
    if encoding_issues:
        print(f"[!] {len(encoding_issues)} files not UTF-8 decodable:")
        for f in encoding_issues:
            print(f"  - {f}")
    else:
        print("[OK] All package Python files are UTF-8 decodable.")

    # 3. Missing internal modules
    header("MISSING INTERNAL MODULES")
    missing = check_missing_internal_modules(py_files)
    if missing:
        print(f"[!] {len(missing)} missing internal module references:")
        for src, mod, path in missing:
            print(f"  - In {src}: imports {mod} -> expected {path}")
    else:
        print("[OK] No missing internal modules detected.")

    # 4. Dependency graph & circular imports
    header("CIRCULAR IMPORTS")
    graph = build_dep_graph(py_files)
    cycles = detect_circular_imports(graph)
    if cycles:
        print(f"[!] {len(cycles)} circular import chains found:")
        for chain in cycles:
            print("  - " + " -> ".join(chain))
    else:
        print("[OK] No circular imports detected.")

    # 5. Orphan Python files
    header("ORPHAN PYTHON FILES")
    orphans = check_orphan_files(py_files)
    if orphans:
        print(f"[!] {len(orphans)} orphan Python files under src/:")
        for f in orphans:
            print(f"  - {f}")
    else:
        print("[OK] No orphan Python files under src/.")

    # 6. Runtime artifacts
    header("RUNTIME ARTIFACTS")
    artifacts = check_runtime_artifacts()
    if artifacts:
        print(f"[INFO] {len(artifacts)} runtime artifacts found under runtime/:")
        for f in artifacts:
            print(f"  - {f}")
    else:
        print("[OK] No runtime artifacts found (runtime/ is clean or missing).")

    # 7. Templates & static
    header("TEMPLATES & STATIC CHECK")
    ts_issues = check_templates_and_static()
    if ts_issues:
        for kind, path in ts_issues:
            print(f"[!] {kind}: {path}")
    else:
        print("[OK] templates/ and static/ present under package.")

    # 8. Config files
    header("CONFIG CHECK")
    cfg_issues = check_config_files()
    if cfg_issues:
        for kind, path in cfg_issues:
            print(f"[!] {kind}: {path}")
    else:
        print("[OK] Config directory and key files present.")

    # 9. Requirements
    header("REQUIREMENTS CHECK")
    req_issues = check_requirements()
    if req_issues:
        for msg in req_issues:
            print(f"[!] {msg}")
    else:
        print("[OK] requirements.txt and requirements.lock present.")

    header("SUMMARY")
    summary = {
        "encoding_issues": len(encoding_issues),
        "missing_internal_modules": len(missing),
        "circular_import_chains": len(cycles),
        "orphan_py_files": len(orphans),
        "runtime_artifacts": len(artifacts),
        "templates_static_issues": len(ts_issues),
        "config_issues": len(cfg_issues),
        "requirements_issues": len(req_issues),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
