#!/usr/bin/env python3
"""
Makefile Drift Validator
Path: ssrf-command-console/tools/validate_makefile.py

Enforces:
- Canonical mk/ include order
- Target naming conventions
- Grouping and ordering rules
- Duplicate target detection
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"
MK_DIR = ROOT / "mk"

# ============================================================
# Canonical include order
# ============================================================

CANONICAL_INCLUDES = [
    "mk/banners.mk",
    "mk/colors.mk",
    "mk/paths.mk",
    "mk/env.mk",
    "mk/python.mk",
    "mk/superdoctor.mk",
    "mk/validate.mk",
]

# ============================================================
# Helpers
# ============================================================


def fail(msg):
    print(f"::error::{msg}")
    sys.exit(1)


def load_makefile():
    if not MAKEFILE.exists():
        fail("Root Makefile missing")
    return MAKEFILE.read_text().splitlines()


def extract_includes(lines):
    return [line.strip().split()[1] for line in lines if line.startswith("include ")]


def extract_targets(lines):
    pattern = re.compile(r"^([a-zA-Z0-9\-_]+):")
    return [pattern.match(line).group(1) for line in lines if pattern.match(line)]


# ============================================================
# Validation Steps
# ============================================================


def validate_include_order(includes):
    if includes != CANONICAL_INCLUDES:
        fail(
            "mk/ include order drift detected.\n"
            f"Expected:\n  {CANONICAL_INCLUDES}\n"
            f"Found:\n  {includes}"
        )


def validate_target_naming(targets):
    for t in targets:
        if t != t.lower():
            fail(f"Target '{t}' must be lowercase")
        if " " in t:
            fail(f"Target '{t}' contains spaces")
        if t.count("_") > 3:
            fail(f"Target '{t}' contains excessive underscores")


def validate_duplicate_targets(targets):
    seen = set()
    for t in targets:
        if t in seen:
            fail(f"Duplicate target detected: {t}")
        seen.add(t)


# ============================================================
# Main
# ============================================================


def main():
    print("=== Validating Makefile Structure ===")

    lines = load_makefile()
    includes = extract_includes(lines)
    targets = extract_targets(lines)

    validate_include_order(includes)
    validate_target_naming(targets)
    validate_duplicate_targets(targets)

    print("Makefile structure OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
