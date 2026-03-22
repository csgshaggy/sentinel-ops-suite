#!/usr/bin/env python3
"""
makefile_integrity_validator.py

Ensures the Makefile has not drifted from the expected operator‑grade structure.
This validator checks:

- Required section banners
- Required targets
- Required ordering
- No missing or renamed sections
- No accidental deletions
"""

import sys
from pathlib import Path

REQUIRED_BANNERS = [
    "SSRF COMMAND CONSOLE — OPERATOR-GRADE MAKEFILE",
    "SECTION 1 — NEW TARGETS",
    "SECTION 2 — UV INTEGRATION",
    "SECTION 2 — POETRY INTEGRATION",
    "SECTION 3 — DOCKER BUILD/RUN TARGETS",
    "SECTION 4 — CI-AWARE GATES",
    "SECTION 5 — FULL UNINSTALL SUITE",
]

REQUIRED_TARGETS = [
    "help:",
    "self-check:",
    "bootstrap:",
    "repair:",
    "env-inspect:",
    "deps:",
    "plugins:",
    "release:",
    "format:",
    "lint:",
    "test:",
    "clean:",
    "rebuild:",
    "uv-bootstrap:",
    "uv-sync:",
    "uv-run:",
    "poetry-bootstrap:",
    "poetry-lock:",
    "poetry-run:",
    "docker-build:",
    "docker-run:",
    "docker-shell:",
    "docker-clean:",
    "docker-rebuild:",
    "ci-check:",
    "ci-fast:",
    "ci-strict:",
    "ci-security:",
    "ci-precommit:",
    "uninstall-env:",
    "uninstall-docker:",
    "uninstall-hooks:",
    "uninstall-cache:",
    "uninstall:",
]

def fail(msg):
    print(f"[ERROR] {msg}")
    sys.exit(1)

def main():
    makefile_path = Path("Makefile")

    if not makefile_path.exists():
        fail("Makefile not found in project root.")

    content = makefile_path.read_text()

    # Check banners
    for banner in REQUIRED_BANNERS:
        if banner not in content:
            fail(f"Missing required banner: {banner}")

    # Check targets
    for target in REQUIRED_TARGETS:
        if target not in content:
            fail(f"Missing required target: {target}")

    # Optional: enforce ordering
    last_index = -1
    for banner in REQUIRED_BANNERS:
        idx = content.find(banner)
        if idx == -1:
            fail(f"Banner not found: {banner}")
        if idx < last_index:
            fail(f"Banner out of order: {banner}")
        last_index = idx

    print("[OK] Makefile integrity validated successfully.")

if __name__ == "__main__":
    main()
