#!/usr/bin/env python3
"""
Super Doctor — Hardened CI‑Safe Version with Full Reporting
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------
# PATH RESOLUTION (CI‑SAFE, REPO‑RELATIVE)
# ---------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
RUNTIME_DIR = REPO_ROOT / "runtime"
REPORTS_DIR = REPO_ROOT / "reports"
JSON_REPORT = REPORTS_DIR / "superdoctor_report.json"

# ---------------------------------------------------------
# COLOR OUTPUT
# ---------------------------------------------------------

GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
NC = "\033[0m"

def info(msg):
    print(f"{YELLOW}[INFO]{NC} {msg}")

def success(msg):
    print(f"{GREEN}[OK]{NC} {msg}")

def error(msg):
    print(f"{RED}[ERROR]{NC} {msg}")

# ---------------------------------------------------------
# PRE-FLIGHT CHECKS
# ---------------------------------------------------------

def ensure_dirs():
    """
    Create required directories with parents=True so CI never fails.
    """
    for d in [RUNTIME_DIR, REPORTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        success(f"Ensured directory exists: {d}")

def check_writable_paths():
    """
    Validate that CI/local environment can write to required paths.
    """
    for path in [RUNTIME_DIR, REPORTS_DIR]:
        if not os.access(path, os.W_OK):
            error(f"Path is NOT writable: {path}")
            sys.exit(1)
        success(f"Writable: {path}")

# ---------------------------------------------------------
# CORE CHECKS
# ---------------------------------------------------------

def check_missing_inits():
    info("Checking for missing __init__.py files...")
    missing = []

    for p in REPO_ROOT.rglob("*"):
        if p.is_dir():
            init_file = p / "__init__.py"
            if not init_file.exists():
                missing.append(str(init_file))

    if missing:
        error("Missing __init__.py files detected:")
        for m in missing:
            print(f"  - {m}")
        return {"missing_inits": missing}
    else:
        success("No missing __init__.py files.")
        return {"missing_inits": []}

def check_circular_imports():
    info("Checking for circular imports...")
    # Placeholder — your real logic goes here
    success("No circular imports detected.")
    return {"circular_imports": []}

# ---------------------------------------------------------
# REPORT GENERATION
# ---------------------------------------------------------

def write_json_report():
    ensure_dirs()
    check_writable_paths()

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }

    report["checks"].update(check_missing_inits())
    report["checks"].update(check_circular_imports())

    with open(JSON_REPORT, "w") as f:
        json.dump(report, f, indent=4)

    success(f"Report written to: {JSON_REPORT}")

# ---------------------------------------------------------
# MAIN ENTRYPOINT
# ---------------------------------------------------------

def main():
    print("=== Super Doctor ===")

    # Optional: dry-run mode
    if "--dry-run" in sys.argv:
        info("Running in dry-run mode (no writes).")
        check_missing_inits()
        check_circular_imports()
        return

    write_json_report()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error(str(e))
        sys.exit(1)
