#!/usr/bin/env python3
"""
Drift Dashboard Generator

Consumes:
- runtime/drift_results.json

Produces:
- runtime/drift_dashboard.md

This script mirrors the architecture of doctor_dashboard.py
for consistency, predictability, and CI alignment.
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

INPUT_JSON = REPO_ROOT / "runtime" / "drift_results.json"
OUTPUT_MD = REPO_ROOT / "runtime" / "drift_dashboard.md"


# ---------------------------------------------------------
# Dashboard generation
# ---------------------------------------------------------
def generate_dashboard():
    info("Loading drift results...")

    if not INPUT_JSON.exists():
        fail(f"Missing drift results file: {INPUT_JSON}")
        sys.exit(1)

    try:
        data = json.loads(INPUT_JSON.read_text())
    except Exception as e:
        fail(f"Failed to parse drift results: {e}")
        sys.exit(1)

    diffs = data.get("diffs", [])
    timestamp = data.get("timestamp", "unknown")

    info("Generating drift dashboard...")

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_MD.open("w") as f:
        f.write("# Drift Dashboard\n\n")
        f.write(f"Generated: **{datetime.utcnow().isoformat()}Z**\n\n")
        f.write(f"Source Timestamp: `{timestamp}`\n\n")

        # Summary
        f.write("## Summary\n")
        f.write(f"- **Total Drift Events:** {len(diffs)}\n")
        f.write(f"- **Status:** {'Drift Detected' if diffs else 'No Drift'}\n\n")

        # Detailed results
        f.write("## Detailed Drift\n")
        if not diffs:
            f.write("No drift detected.\n")
        else:
            for d in diffs:
                dtype = d.get("type", "unknown")
                key = d.get("key", "unknown")

                icon = {
                    "added": "🟢",
                    "removed": "🔴",
                    "changed": "🟡",
                }.get(dtype, "⚪")

                f.write(f"### {icon} {dtype.upper()}: `{key}`\n")

                if dtype == "changed":
                    f.write(f"- **Baseline:** `{d.get('baseline')}`\n")
                    f.write(f"- **Current:** `{d.get('current')}`\n\n")
                else:
                    f.write(f"- **Value:** `{d.get('value')}`\n\n")

    ok("Drift dashboard generated successfully.")


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        generate_dashboard()
    except Exception as e:
        fail(str(e))
        sys.exit(1)
