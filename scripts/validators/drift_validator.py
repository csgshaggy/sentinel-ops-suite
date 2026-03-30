#!/usr/bin/env python3
"""
SSRF Command Console — Drift-Aware Validator
Canonical Makefile + mk/ layout enforcement.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "Makefile",
    "mk/core.mk",
    "mk/docs.mk",
    "mk/validate.mk",
    "mk/util.mk",
    "mk/audit.mk",
    "mk/release.mk",
    "mk/env.mk",
]

ALLOWED_MK_FILES = {
    "core.mk",
    "docs.mk",
    "validate.mk",
    "util.mk",
    "audit.mk",
    "release.mk",
    "env.mk",
}


def main() -> int:
    print("=== SSRF Command Console — Drift-Aware Validator ===\n")

    missing = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            missing.append(rel)

    if missing:
        print("[DRIFT] Missing required files:")
        for m in missing:
            print(f"  - {m}")
        print("\n[FAIL] Structural drift detected. See details above.")
        return 1

    mk_dir = ROOT / "mk"
    unexpected = []
    if mk_dir.exists():
        for p in mk_dir.glob("*.mk"):
            if p.name not in ALLOWED_MK_FILES:
                unexpected.append(p.name)

    if unexpected:
        print("[DRIFT] Unexpected mk/*.mk files detected:")
        for name in unexpected:
            print(f"  - {name}")
        print("\n[FAIL] Structural drift detected. See details above.")
        return 1

    print("[OK] No structural drift detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
