"""
SuperDoctor Plugin: Environment Variable Auditor
Location: tools/plugins/env_vars.py

Checks:
- Missing expected environment variables
- Suspicious or empty values
- Overly long PATH
- Unsafe PATH entries
- Variables with extremely large values
- Cross-platform safe
"""

import os
from pathlib import Path
from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Expected environment variables (customizable)
# ------------------------------------------------------------

EXPECTED_VARS = [
    "HOME",
    "PATH",
    "PYTHONPATH",
    "VIRTUAL_ENV",
]


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _unsafe_path_entries(path_value: str) -> List[str]:
    """
    Detect unsafe PATH entries:
    - current directory ('.')
    - world-writable directories
    - nonexistent directories
    """
    bad = []
    for entry in path_value.split(os.pathsep):
        if not entry:
            continue

        p = Path(entry)

        if entry == ".":
            bad.append(". (current directory in PATH)")
        elif not p.exists():
            bad.append(f"{entry} (missing)")
        else:
            try:
                mode = p.stat().st_mode
                if mode & 0o002:  # world-writable
                    bad.append(f"{entry} (world-writable)")
            except Exception:
                pass

    return bad


def _large_vars(env: dict, threshold: int = 4096) -> List[str]:
    """
    Detect environment variables with extremely large values.
    """
    large = []
    for k, v in env.items():
        if len(v) > threshold:
            large.append(f"{k} ({len(v)} bytes)")
    return large


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root=None) -> List[CheckResult]:
    results: List[CheckResult] = []

    env = dict(os.environ)

    # ------------------------------------------------------------
    # 1. Missing expected environment variables
    # ------------------------------------------------------------
    missing = [var for var in EXPECTED_VARS if var not in env]

    if missing:
        results.append(
            CheckResult(
                id="env.missing",
                name="Missing environment variables",
                description="Some expected environment variables are not set.",
                status="warn",
                severity="medium",
                details="\n".join(missing),
                plugin="env_vars",
            )
        )
    else:
        results.append(
            CheckResult(
                id="env.missing.none",
                name="All expected variables present",
                description="All expected environment variables are set.",
                status="ok",
                severity="info",
                plugin="env_vars",
            )
        )

    # ------------------------------------------------------------
    # 2. Suspicious or empty values
    # ------------------------------------------------------------
    empty = [k for k, v in env.items() if v.strip() == ""]

    if empty:
        results.append(
            CheckResult(
                id="env.empty",
                name="Empty environment variables",
                description="Some environment variables are set but empty.",
                status="warn",
                severity="low",
                details="\n".join(empty),
                plugin="env_vars",
            )
        )
    else:
        results.append(
            CheckResult(
                id="env.empty.none",
                name="No empty variables",
                description="No environment variables are empty.",
                status="ok",
                severity="info",
                plugin="env_vars",
            )
        )

    # ------------------------------------------------------------
    # 3. PATH analysis
    # ------------------------------------------------------------
    path_value = env.get("PATH", "")

    if len(path_value) > 4096:
        results.append(
            CheckResult(
                id="env.path.too_long",
                name="PATH too long",
                description="PATH exceeds 4096 characters.",
                status="warn",
                severity="medium",
                details=f"Length: {len(path_value)} bytes",
                plugin="env_vars",
            )
        )

    bad_entries = _unsafe_path_entries(path_value)

    if bad_entries:
        results.append(
            CheckResult(
                id="env.path.unsafe",
                name="Unsafe PATH entries",
                description="Some PATH entries are unsafe.",
                status="warn",
                severity="high",
                details="\n".join(bad_entries),
                plugin="env_vars",
            )
        )
    else:
        results.append(
            CheckResult(
                id="env.path.ok",
                name="PATH entries safe",
                description="No unsafe PATH entries detected.",
                status="ok",
                severity="info",
                plugin="env_vars",
            )
        )

    # ------------------------------------------------------------
    # 4. Extremely large environment variables
    # ------------------------------------------------------------
    large = _large_vars(env)

    if large:
        results.append(
            CheckResult(
                id="env.large",
                name="Large environment variables",
                description="Some environment variables have unusually large values.",
                status="warn",
                severity="medium",
                details="\n".join(large),
                plugin="env_vars",
            )
        )
    else:
        results.append(
            CheckResult(
                id="env.large.none",
                name="No large variables",
                description="No unusually large environment variables detected.",
                status="ok",
                severity="info",
                plugin="env_vars",
            )
        )

    return results
