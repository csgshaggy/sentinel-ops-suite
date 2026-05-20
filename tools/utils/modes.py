"""
SuperDoctor Mode System
Location: tools/utils/modes.py

Defines:
- Mode enum (STRICT, BALANCED)
- resolve_mode() helper
- mode_allows_check() for plugin-level filtering

Modes influence:
- Health scoring (strict penalizes more)
- Whether certain checks run
- CI behavior (strict fails faster)
"""

from enum import Enum


class Mode(Enum):
    STRICT = "strict"
    BALANCED = "balanced"


# ------------------------------------------------------------
# Mode resolution
# ------------------------------------------------------------


def resolve_mode(value: str) -> Mode:
    """
    Convert a string ("strict" or "balanced") into a Mode enum.
    Defaults to BALANCED for safety.
    """
    value = value.lower().strip()
    if value == "strict":
        return Mode.STRICT
    return Mode.BALANCED


# ------------------------------------------------------------
# Plugin-level mode filtering
# ------------------------------------------------------------


def mode_allows_check(mode: Mode, severity: str) -> bool:
    """
    Determine whether a check should run under the given mode.

    Rules:
    - STRICT: run everything
    - BALANCED: skip low-severity checks to reduce noise

    Plugins can call this to decide whether to skip a check.
    """
    if mode == Mode.STRICT:
        return True

    # Balanced mode skips low-severity checks
    if severity in ("info", "low"):
        return False

    return True
