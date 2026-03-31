#!/usr/bin/env python3
"""
Doctor Dashboard Generator

Produces:
- runtime/doctor_results.json
- runtime/doctor_dashboard.md

Consumes:
- scripts/doctor/run_doctor.py output
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------
# Color helpers (CI-safe)
# ---------------------------------------------------------
class C:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"


def info(msg):
    print(f"{C.BLUE}[INFO]{C.END} {msg}")


def ok(msg):
    print(f"{C.GREEN}[OK]{C.END} {msg}")


def warn(msg):
    print(f"{C.YELLOW}[WARN]{C.END} {msg}")


def fail(msg):
    print(f"{C.RED}[FAIL]{C.END} {msg}")


# ---------------------------------------------------------
# Path resolution
# ---------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
CI_DIR = THIS_FILE.parent
SCRIPTS_DIR = CI_DIR.parent
REPO_ROOT = SCRIPTS_DIR.parent

DOCTOR_SCRIPT = SCRIPTS_DIR / "doctor" / "run_doctor.py"

OUTPUT_DIR = REPO_ROOT / "runtime"
OUTPUT_JSON = OUTPUT_DIR / "doctor_results.json"
OUTPUT_MD = OUTPUT_DIR / "doctor_dashboard.md"


# ---------------------------------------------------------
# Import doctor system
# ---------------------------------------------------------
sys.path.append(str(SCRIPTS_DIR))

try:
    from doctor.run_doctor import run_doctor  # noqa: E402
except Exception as e:
    fail(f"Unable to import doctor system: {e}")
    sys.exit(1)


# ---------------------------------------------------------
# Dashboard generation
# ---------------------------------------------------------
def generate_dashboard():
    info("Running doctor system...")
    results = run_doctor()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # JSON output
    info(f"Writing JSON results → {OUTPUT_JSON}")
    with OUTPUT_JSON.open("w") as f:
        json.dump(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "results": results,
            },
            f,
            indent=2,
        )

    # Markdown dashboard
    info(f"Writing Markdown dashboard → {OUTPUT_MD}")
    with OUTPUT_MD.open("w") as f:
        f.write("# Doctor Dashboard\n\n")
        f.write(f"Generated: **{datetime.utcnow().isoformat()}Z**\n\n")

        f.write("## Summary\n")
        total = len(results)
        passed = sum(1 for r in results if r.get("status") == "pass")
        failed = sum(1 for r in results if r.get("status") == "fail")
        warnings = sum(1 for r in results if r.get("status") == "warn")

        f.write(f"- **Total Checks:** {total}\n")
        f.write(f"- **Passed:** {passed}\n")
        f.write(f"- **Warnings:** {warnings}\n")
        f.write(f"- **Failed:** {failed}\n\n")

        f.write("## Detailed Results\n")
        for r in results:
            name = r.get("name", "Unnamed Check")
            status = r.get("status", "unknown")
            message = r.get("message", "")

            icon = {
                "pass": "🟢",
                "fail": "🔴",
                "warn": "🟡",
            }.get(status, "⚪")

            f.write(f"### {icon} {name}\n")
            f.write(f"**Status:** `{status}`\n\n")
            if message:
                f.write(f"**Message:** {message}\n\n")

    ok("Doctor dashboard generated successfully.")


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        generate_dashboard()
    except Exception as e:
        fail(str(e))
        sys.exit(1)
