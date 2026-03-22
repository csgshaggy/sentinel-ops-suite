"""
Makefile-related doctor checks.

These checks validate:
- Makefile presence
- Required targets
- Structural consistency

Each check returns:
{
    "name": "Check Name",
    "status": "pass" | "fail" | "warn",
    "message": "Human-readable explanation"
}
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------
def result(name: str, status: str, message: str) -> Dict[str, str]:
    return {
        "name": name,
        "status": status,
        "message": message,
    }


# ---------------------------------------------------------
# Repo root resolution
# ---------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[3]


# ---------------------------------------------------------
# Makefile Checks
# ---------------------------------------------------------

def check_makefile_exists() -> Dict[str, str]:
    """Ensure Makefile exists at repo root."""
    path = REPO_ROOT / "Makefile"
    if path.exists():
        return result(
            "Makefile Exists",
            "pass",
            "Makefile is present."
        )
    return result(
        "Makefile Exists",
        "fail",
        "Makefile is missing."
    )


def check_makefile_targets() -> Dict[str, str]:
    """Ensure required Makefile targets exist."""
    required_targets = [
        "doctor",
        "baseline",
        "drift",
        "drift-dashboard",
        "ci-drift",
        "ci-doctor",
        "clean-runtime",
    ]

    path = REPO_ROOT / "Makefile"
    if not path.exists():
        return result(
            "Makefile Targets",
            "fail",
            "Makefile is missing entirely."
        )

    text = path.read_text()
    missing = [t for t in required_targets if f"{t}:" not in text]

    if missing:
        return result(
            "Makefile Targets",
            "fail",
            f"Missing Makefile target(s): {', '.join(missing)}"
        )

    return result(
        "Makefile Targets",
        "pass",
        "All required Makefile targets are present."
    )


def check_makefile_formatting() -> Dict[str, str]:
    """
    Basic formatting expectations:
    - Tabs used for recipes
    - No CRLF line endings
    - No trailing whitespace on recipe lines
    """
    path = REPO_ROOT / "Makefile"
    if not path.exists():
        return result(
            "Makefile Formatting",
            "fail",
            "Makefile is missing."
        )

    text = path.read_text()

    # Check for CRLF
    if "\r\n" in text:
        return result(
            "Makefile Formatting",
            "warn",
            "Makefile contains CRLF line endings."
        )

    # Check for tabs in recipes
    lines = text.splitlines()
    missing_tabs = [
        line for line in lines
        if line.strip() and not line.startswith("\t") and ":" not in line and "=" not in line
    ]

    if missing_tabs:
        return result(
            "Makefile Formatting",
            "warn",
            "Some recipe lines may not start with a tab."
        )

    return result(
        "Makefile Formatting",
        "pass",
        "Makefile formatting appears clean."
    )
