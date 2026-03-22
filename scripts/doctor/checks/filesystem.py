"""
Filesystem-related doctor checks.

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
# Filesystem Checks
# ---------------------------------------------------------

def check_runtime_directory() -> Dict[str, str]:
    """Ensure runtime/ exists."""
    path = REPO_ROOT / "runtime"
    if path.exists():
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
    path = REPO_ROOT / "runtime"
    if not path.exists():
        return result(
            "Runtime Hygiene",
            "warn",
            "runtime/ directory does not exist yet."
        )

    bad = [
        p.name for p in path.iterdir()
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


def check_required_directories() -> Dict[str, str]:
    """Ensure core directories exist."""
    required = [
        "scripts",
        "scripts/ci",
        "scripts/doctor",
        "runtime",
        "docs",
        ".github/workflows",
        ".github/scripts",
    ]

    missing = [d for d in required if not (REPO_ROOT / d).exists()]

    if missing:
        return result(
            "Required Directories Present",
            "fail",
            f"Missing directory(ies): {', '.join(missing)}"
        )

    return result(
        "Required Directories Present",
        "pass",
        "All required directories are present."
    )
