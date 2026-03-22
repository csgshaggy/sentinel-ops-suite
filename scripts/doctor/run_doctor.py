#!/usr/bin/env python3
"""
Doctor System (Modular Version)

Runs a suite of repository health checks and returns
structured results for dashboards and CI workflows.

Each check returns:
{
    "name": "Check Name",
    "status": "pass" | "fail" | "warn",
    "message": "Human-readable explanation"
}
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Dict

# ---------------------------------------------------------
# Color helpers (safe for CI)
# ---------------------------------------------------------
class C:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"

def info(msg): print(f"{C.BLUE}[INFO]{C.END} {msg}")
def ok(msg): print(f"{C.GREEN}[OK]{C.END} {msg}")
def warn(msg): print(f"{C.YELLOW}[WARN]{C.END} {msg}")
def fail(msg): print(f"{C.RED}[FAIL]{C.END} {msg}")


# ---------------------------------------------------------
# Repo root resolution
# ---------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKS_DIR = REPO_ROOT / "scripts" / "doctor" / "checks"

# Add checks directory to PYTHONPATH
sys.path.append(str(CHECKS_DIR))


# ---------------------------------------------------------
# Import modular checks
# ---------------------------------------------------------
from filesystem import (
    check_runtime_directory,
    check_runtime_hygiene,
    check_required_directories,
)

from structure import (
    check_required_scripts,
    check_required_workflows,
    check_docs_directory,
    check_github_structure,
)

from makefile import (
    check_makefile_exists,
    check_makefile_targets,
    check_makefile_formatting,
)

from runtime import (
    check_expected_artifacts,
)


# ---------------------------------------------------------
# Registry of all doctor checks
# ---------------------------------------------------------
CHECKS = [
    # Filesystem
    check_runtime_directory,
    check_runtime_hygiene,
    check_required_directories,

    # Structure
    check_required_scripts,
    check_required_workflows,
    check_docs_directory,
    check_github_structure,

    # Makefile
    check_makefile_exists,
    check_makefile_targets,
    check_makefile_formatting,

    # Runtime artifacts
    check_expected_artifacts,
]


# ---------------------------------------------------------
# Main doctor runner
# ---------------------------------------------------------
def run_doctor() -> List[Dict[str, str]]:
    info("Running modular doctor checks...")

    results = []

    for check in CHECKS:
        try:
            r = check()
            results.append(r)

            status = r["status"]
            name = r["name"]

            if status == "pass":
                ok(name)
            elif status == "warn":
                warn(name)
            else:
                fail(name)

        except Exception as e:
            results.append({
                "name": check.__name__,
                "status": "fail",
                "message": f"Check crashed: {e}",
            })
            fail(f"{check.__name__} crashed: {e}")

    return results


# ---------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------
if __name__ == "__main__":
    run_doctor()
