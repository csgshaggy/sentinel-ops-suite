"""
Router Prefix Drift Detector Plugin
Scans all FastAPI router files for prefix violations relative to the SentinelOps model.
"""

from pathlib import Path
import ast
from typing import Dict, List, Any


EXPECTED_PREFIXES = {
    "auth": "/auth",
    "users": "/users",
    "admin": "/admin",
    "sessions": "/sessions",
    "stream": "/stream",
    "plugins": "/plugins",
    "repo": "/repo",
    "ci": "/ci",
    "workflow-runs": "/workflow-runs",
    "router-drift": "/plugins",  # special case
}


class RouterPrefixVisitor(ast.NodeVisitor):
    def __init__(self):
        self.prefixes = []

    def visit_Call(self, node):
        # Look for APIRouter(prefix="...")
        if isinstance(node.func, ast.Name) and node.func.id == "APIRouter":
            for kw in node.keywords:
                if kw.arg == "prefix" and isinstance(kw.value, ast.Constant):
                    self.prefixes.append(kw.value.value)
        self.generic_visit(node)


def scan_router_file(path: Path) -> Dict[str, Any]:
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError:
        return {"file": str(path), "error": "syntax_error", "prefixes": []}

    visitor = RouterPrefixVisitor()
    visitor.visit(tree)

    return {
        "file": str(path),
        "prefixes": visitor.prefixes,
    }


def detect_prefix_drift(root: Path) -> Dict[str, Any]:
    router_dir = root / "backend" / "app" / "routers"
    results = []
    violations = []

    for py_file in router_dir.rglob("*.py"):
        info = scan_router_file(py_file)
        results.append(info)

        for prefix in info["prefixes"]:
            # Rule 1: No router may contain /api in its prefix
            if prefix.startswith("/api"):
                violations.append({
                    "file": str(py_file),
                    "prefix": prefix,
                    "reason": "Router prefix must not include /api (main.py applies it globally)."
                })

            # Rule 2: Prefix must start with a slash
            if not prefix.startswith("/"):
                violations.append({
                    "file": str(py_file),
                    "prefix": prefix,
                    "reason": "Router prefix must start with '/'."
                })

            # Rule 3: Check against expected model
            stem = py_file.stem.replace("_router", "").replace("_", "-")
            expected = EXPECTED_PREFIXES.get(stem)

            if expected and prefix != expected:
                violations.append({
                    "file": str(py_file),
                    "prefix": prefix,
                    "expected": expected,
                    "reason": "Prefix does not match SentinelOps routing model."
                })

    status = "ok" if not violations else "drift"

    return {
        "status": status,
        "violations": violations,
        "scanned": results,
    }


def run() -> Dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    return detect_prefix_drift(root)
