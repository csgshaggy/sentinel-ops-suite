#!/usr/bin/env python3
"""
Drift-aware structure validator for SSRF Command Console.

Focus: canonical paths, required files, and obvious structural drift.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = [
    "Makefile",
    "backend",
    "dashboard",
    "scripts",
    "scripts/canonical",
    "scripts/validators",
    "src",
    "src/ssrf_command_console",
    "mk",
]

REQUIRED_FILES = [
    "Makefile",
    "scripts/structure_validator.py",
    "scripts/safe_clean.sh",
    "mk/core.mk",
    "mk/env.mk",
    "mk/docs.mk",
    "mk/release.mk",
    "mk/validate.mk",
]

def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)

def check_required_paths():
    missing = []
    for rel_path in REQUIRED_PATHS:
        p = ROOT / rel_path
        if not p.exists():
            missing.append(rel_path)
    return missing

def check_required_files():
    missing = []
    for rel_path in REQUIRED_FILES:
        p = ROOT / rel_path
        if not p.is_file():
            missing.append(rel_path)
    return missing

def main() -> int:
    print("=== SSRF Command Console — Drift-Aware Validator ===")
    missing_paths = check_required_paths()
    missing_files = check_required_files()

    had_error = False

    if missing_paths:
        had_error = True
        print("\n[DRIFT] Missing required paths:")
        for p in missing_paths:
            print(f"  - {p}")

    if missing_files:
        had_error = True
        print("\n[DRIFT] Missing required files:")
        for f in missing_files:
            print(f"  - {f}")

    if not had_error:
        print("\n[OK] No structural drift detected.")
        return 0

    print("\n[FAIL] Structural drift detected. See details above.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
