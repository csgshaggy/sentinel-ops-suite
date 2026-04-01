#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path("backend/app")
PELM = ROOT / "pelm"

REQUIRED_DIRS = [
    ROOT,
    PELM,
]

REQUIRED_FILES = [
    ROOT / "main.py",
    PELM / "pelm_status.py",
    PELM / "pelm_run.py",
    PELM / "pelm_trend.py",
    PELM / "pelm_snapshots.py",
    PELM / "pelm_regression.py",
    PELM / "pelm_governance.py",
    PELM / "pelm_report.py",
]

ALLOWED_PELM = {
    "pelm_status.py",
    "pelm_run.py",
    "pelm_trend.py",
    "pelm_snapshots.py",
    "pelm_regression.py",
    "pelm_governance.py",
    "pelm_report.py",
    "__init__.py",
}

def fail(msg):
    print(f"[BACKEND STRUCTURE ERROR] {msg}")
    sys.exit(1)

def main():
    # Required directories
    for d in REQUIRED_DIRS:
        if not d.exists():
            fail(f"Missing directory: {d}")

    # Required files
    for f in REQUIRED_FILES:
        if not f.exists():
            fail(f"Missing file: {f}")

    # Unexpected files in pelm/
    for f in PELM.iterdir():
        if f.is_file() and f.name not in ALLOWED_PELM:
            fail(f"Unexpected file in pelm/: {f.name}")

    print("[OK] Backend structure is valid and drift‑free.")

if __name__ == "__main__":
    main()
