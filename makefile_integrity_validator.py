#!/usr/bin/env python
import sys
from pathlib import Path

REQUIRED_BANNERS = [
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


def fail(msg: str) -> None:
    print(f"[ERROR] {msg}")
    sys.exit(1)


def main() -> None:
    makefile_path = Path("Makefile")
    if not makefile_path.exists():
        fail("Makefile not found in project root.")

    content = makefile_path.read_text()

    # Banners present
    for banner in REQUIRED_BANNERS:
        if banner not in content:
            fail(f"Missing required banner: {banner}")

    # Banners in order
    last_idx = -1
    for banner in REQUIRED_BANNERS:
        idx = content.find(banner)
        if idx == -1:
            fail(f"Banner not found: {banner}")
        if idx < last_idx:
            fail(f"Banner out of order: {banner}")
        last_idx = idx

    # Targets present
    for target in REQUIRED_TARGETS:
        if target not in content:
            fail(f"Missing required target: {target}")

    # Format target must reference black + prettier
    if "format:" not in content or "black" not in content or "prettier" not in content:
        fail("format target must reference both black and prettier.")

    # Drift target must call validate-structure and use --check
    if "drift:" not in content:
        fail("Missing drift target.")
    if "validate-structure" not in content:
        fail("drift target must call validate-structure.")
    if "--check" not in content:
        fail("drift target must use --check for formatters.")

    # self-check must call validate-structure and drift
    if (
        "self-check:" not in content
        or "validate-structure" not in content
        or "drift" not in content
    ):
        fail("self-check target must call validate-structure and drift.")

    print("[OK] Makefile integrity validated successfully.")


if __name__ == "__main__":
    main()
