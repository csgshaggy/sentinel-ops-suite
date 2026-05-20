"""
Structure-related doctor checks.

These checks validate:
- required scripts
- required CI workflow files
- required project directories
- structural consistency across the repo

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
# Structure Checks
# ---------------------------------------------------------


def check_required_scripts() -> Dict[str, str]:
    """Ensure all core scripts exist."""
    required = [
        "scripts/drift_detector.py",
        "scripts/ci/drift_dashboard.py",
        "scripts/ci/doctor_dashboard.py",
        "scripts/doctor/run_doctor.py",
    ]

    missing = [f for f in required if not (REPO_ROOT / f).exists()]

    if missing:
        return result(
            "Required Scripts Present",
            "fail",
            f"Missing script(s): {', '.join(missing)}",
        )

    return result(
        "Required Scripts Present", "pass", "All required scripts are present."
    )


def check_required_workflows() -> Dict[str, str]:
    """Ensure core GitHub Actions workflows exist."""
    required = [
        ".github/workflows/drift-dashboard.yml",
        ".github/workflows/doctor-cleanup.yml",
        ".github/workflows/doctor-dashboard.yml",
        ".github/workflows/repo-integrity.yml",
        ".github/workflows/super-doctor-balanced-gate.yml",
        ".github/workflows/super-doctor-ci-gate.yml",
    ]

    missing = [f for f in required if not (REPO_ROOT / f).exists()]

    if missing:
        return result(
            "Required Workflows Present",
            "fail",
            f"Missing workflow(s): {', '.join(missing)}",
        )

    return result(
        "Required Workflows Present", "pass", "All required workflows are present."
    )


def check_docs_directory() -> Dict[str, str]:
    """Ensure docs/ exists and is a directory."""
    path = REPO_ROOT / "docs"
    if not path.exists():
        return result("Docs Directory Exists", "warn", "docs/ directory is missing.")
    if not path.is_dir():
        return result(
            "Docs Directory Exists", "fail", "docs/ exists but is not a directory."
        )
    return result("Docs Directory Exists", "pass", "docs/ directory is present.")


def check_github_structure() -> Dict[str, str]:
    """Ensure .github/ structure is correct."""
    required = [
        ".github",
        ".github/workflows",
        ".github/scripts",
    ]

    missing = [d for d in required if not (REPO_ROOT / d).exists()]

    if missing:
        return result(
            "GitHub Directory Structure",
            "fail",
            f"Missing GitHub directory(ies): {', '.join(missing)}",
        )

    return result(
        "GitHub Directory Structure", "pass", "GitHub directory structure is valid."
    )
