"""
tools/doctor.py
Operator-grade repository health checker.

Runs:
- Python version check
- Dependency drift detection
- Plugin registry validation
- Directory structure validation
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent


def check_python_version() -> Dict[str, Any]:
    return {
        "expected": "3.12",
        "actual": f"{sys.version_info.major}.{sys.version_info.minor}",
        "ok": sys.version_info >= (3, 12),
    }


def check_dependencies() -> Dict[str, Any]:
    """Check pip for outdated packages."""
    try:
        result = subprocess.run(
            ["pip", "list", "--outdated", "--format=json"],
            capture_output=True,
            text=True,
            check=True,
        )
        import json

        outdated = json.loads(result.stdout)
        return {"outdated": outdated, "ok": len(outdated) == 0}
    except Exception as exc:
        return {"error": str(exc), "ok": False}


def check_structure() -> Dict[str, Any]:
    """Ensure required directories exist."""
    required = [
        ROOT / "tools",
        ROOT / "tools" / "plugins",
        ROOT / "backend",
        ROOT / "scripts",
    ]

    missing = [str(p) for p in required if not p.exists()]
    return {"missing": missing, "ok": len(missing) == 0}


def check_plugins() -> Dict[str, Any]:
    """Use plugin_loader to validate plugins."""
    try:
        from tools.plugin_loader import validate_plugins

        results = validate_plugins()
        bad = {k: v for k, v in results.items() if v != "OK"}
        return {"bad_plugins": bad, "ok": len(bad) == 0}
    except Exception as exc:
        return {"error": str(exc), "ok": False}


def print_section(title: str):
    print("\n" + "=" * 60)
    print(f"{title}")
    print("=" * 60)


def main():
    print_section("🔧 SSRF Command Console — Doctor Report")

    # Python version
    print_section("Python Version")
    py = check_python_version()
    print(py)

    # Dependencies
    print_section("Dependency Drift")
    deps = check_dependencies()
    print(deps)

    # Structure
    print_section("Directory Structure")
    struct = check_structure()
    print(struct)

    # Plugins
    print_section("Plugin Registry")
    plugins = check_plugins()
    print(plugins)

    print("\nDoctor run complete.\n")


if __name__ == "__main__":
    main()
