#!/usr/bin/env python3
"""
Drift Detector

Compares:
- baseline.json  (expected state)
- current.json   (current state)

Produces:
- runtime/drift_results.json

This script is intentionally simple, deterministic, and
operator-grade. It does not assume any specific schema beyond
JSON-serializable dictionaries.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------
# Color helpers (CI-safe)
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
# Path resolution
# ---------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
SCRIPTS_DIR = THIS_FILE.parent
REPO_ROOT = SCRIPTS_DIR.parent

BASELINE = REPO_ROOT / "baseline.json"
CURRENT = REPO_ROOT / "current.json"

OUTPUT_DIR = REPO_ROOT / "runtime"
OUTPUT_JSON = OUTPUT_DIR / "drift_results.json"


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def load_json(path: Path):
    if not path.exists():
        warn(f"Missing file: {path}")
        return None
    try:
        return json.loads(path.read_text())
    except Exception as e:
        fail(f"Failed to parse {path}: {e}")
        return None


def compare_dicts(baseline: dict, current: dict):
    """
    Simple recursive diff:
    - keys added
    - keys removed
    - values changed
    """
    diffs = []

    baseline_keys = set(baseline.keys())
    current_keys = set(current.keys())

    added = current_keys - baseline_keys
    removed = baseline_keys - current_keys
    common = baseline_keys & current_keys

    for key in sorted(added):
        diffs.append({
            "type": "added",
            "key": key,
            "value": current[key],
        })

    for key in sorted(removed):
        diffs.append({
            "type": "removed",
            "key": key,
            "value": baseline[key],
        })

    for key in sorted(common):
        b = baseline[key]
        c = current[key]

        if isinstance(b, dict) and isinstance(c, dict):
            nested = compare_dicts(b, c)
            for n in nested:
                n["key"] = f"{key}.{n['key']}"
            diffs.extend(nested)
        elif b != c:
            diffs.append({
                "type": "changed",
                "key": key,
                "baseline": b,
                "current": c,
            })

    return diffs


# ---------------------------------------------------------
# Drift detection
# ---------------------------------------------------------
def detect_drift():
    info("Loading baseline and current state...")

    baseline = load_json(BASELINE)
    current = load_json(CURRENT)

    if baseline is None or current is None:
        fail("Cannot perform drift detection without both baseline.json and current.json")
        return []

    info("Comparing baseline → current...")
    diffs = compare_dicts(baseline, current)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    info(f"Writing drift results → {OUTPUT_JSON}")
    OUTPUT_JSON.write_text(json.dumps({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "diffs": diffs,
    }, indent=2))

    if diffs:
        warn(f"Drift detected: {len(diffs)} change(s)")
    else:
        ok("No drift detected.")

    return diffs


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        detect_drift()
    except Exception as e:
        fail(str(e))
        sys.exit(1)
