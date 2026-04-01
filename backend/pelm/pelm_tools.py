import json
import difflib
import sys
from pathlib import Path
from datetime import datetime

from backend.pelm.pelm_canonical import CANONICAL_PELM_PLUGIN

PELM_PATH = Path("backend/pelm/pelm_plugin.py")
SNAPSHOT_DIR = Path("backend/pelm/snapshots")
SNAPSHOT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# Drift Detection
# ---------------------------------------------------------
def detect_pelm_drift() -> dict:
    if not PELM_PATH.exists():
        return {"drift": True, "reason": "PELM plugin missing", "diff": ""}

    current = PELM_PATH.read_text()
    canonical = CANONICAL_PELM_PLUGIN

    diff = list(
        difflib.unified_diff(
            canonical.splitlines(keepends=True),
            current.splitlines(keepends=True),
            fromfile="canonical",
            tofile="current",
        )
    )

    return {
        "drift": len(diff) > 0,
        "diff": "".join(diff),
    }


# ---------------------------------------------------------
# Auto-Repair
# ---------------------------------------------------------
def repair_pelm() -> dict:
    PELM_PATH.write_text(CANONICAL_PELM_PLUGIN)
    return {"repaired": True, "path": str(PELM_PATH)}


# ---------------------------------------------------------
# Contract Validation
# ---------------------------------------------------------
def validate_pelm_contract(output: dict) -> dict:
    required = ["status", "risk", "signals", "metadata"]

    missing = [k for k in required if k not in output]
    if missing:
        return {"valid": False, "missing": missing}

    if "contract" not in output["metadata"]:
        return {"valid": False, "missing": ["metadata.contract"]}

    return {"valid": True}


# ---------------------------------------------------------
# Snapshot System
# ---------------------------------------------------------
def snapshot_pelm_output(output: dict) -> dict:
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    path = SNAPSHOT_DIR / f"pelm-{ts}.json"
    path.write_text(json.dumps(output, indent=2))
    return {"snapshot": str(path)}


# ---------------------------------------------------------
# Regression Detector
# ---------------------------------------------------------
def detect_pelm_regression() -> dict:
    snapshots = sorted(SNAPSHOT_DIR.glob("pelm-*.json"))
    if len(snapshots) < 2:
        return {"regression": False, "reason": "Not enough snapshots"}

    latest = json.loads(snapshots[-1].read_text())
    previous = json.loads(snapshots[-2].read_text())

    if latest.get("risk") != previous.get("risk"):
        return {
            "regression": True,
            "reason": "Risk level changed",
            "previous": previous.get("risk"),
            "current": latest.get("risk"),
        }

    return {"regression": False}


# ---------------------------------------------------------
# CLI Entry (for Makefile targets)
# ---------------------------------------------------------
def _cli():
    if len(sys.argv) < 2:
        print("Usage: pelm_tools.py [drift|repair|regression]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "drift":
        result = detect_pelm_drift()
        print(json.dumps(result, indent=2))
        sys.exit(0 if not result["drift"] else 1)

    if cmd == "repair":
        result = repair_pelm()
        print(json.dumps(result, indent=2))
        sys.exit(0)

    if cmd == "regression":
        result = detect_pelm_regression()
        print(json.dumps(result, indent=2))
        sys.exit(0 if not result["regression"] else 1)

    print(f"Unknown command: {cmd}")
    sys.exit(1)


if __name__ == "__main__":
    _cli()
