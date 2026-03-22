"""
Runtime-related doctor checks.

These checks validate:
- runtime/ directory presence
- hygiene (only .json and .md files)
- expected artifacts (optional future expansion)

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
RUNTIME_DIR = REPO_ROOT / "runtime"


# ---------------------------------------------------------
# Runtime Checks
# ---------------------------------------------------------

def check_runtime_exists() -> Dict[str, str]:
    """Ensure runtime/ directory exists."""
    if RUNTIME_DIR.exists():
        return result(
            "Runtime Directory Exists",
            "pass",
            "runtime/ directory is present."
        )
    return result(
        "Runtime Directory Exists",
        "fail",
        "runtime/ directory is missing."
    )


def check_runtime_hygiene() -> Dict[str, str]:
    """Ensure runtime/ contains only .json and .md files."""
    if not RUNTIME_DIR.exists():
        return result(
            "Runtime Hygiene",
            "warn",
            "runtime/ directory does not exist yet."
        )

    bad = [
        p.name for p in RUNTIME_DIR.iterdir()
        if p.is_file() and p.suffix not in [".json", ".md"]
    ]

    if bad:
        return result(
            "Runtime Hygiene",
            "warn",
            f"Unexpected files in runtime/: {', '.join(bad)}"
        )

    return result(
        "Runtime Hygiene",
        "pass",
        "runtime/ directory is clean."
    )


def check_expected_artifacts() -> Dict[str, str]:
    """
    Validate presence of expected artifacts.
    These are optional — absence is a warning, not a failure.
    """
    expected = [
        "drift_results.json",
        "drift_dashboard.md",
        "doctor_results.json",
        "doctor_dashboard.md",
    ]

    missing = [
        f for f in expected
        if not (RUNTIME_DIR / f).exists()
    ]

    if missing:
        return result(
            "Expected Artifacts Present",
            "warn",
            f"Missing expected artifact(s): {', '.join(missing)}"
        )

    return result(
        "Expected Artifacts Present",
        "pass",
        "All expected runtime artifacts are present."
    )
