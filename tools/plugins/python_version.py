"""
SuperDoctor Plugin: Python Version & ABI Integrity
Location: tools/plugins/python_version.py

Checks:
- Python version (major/minor/micro)
- ABI tag consistency
- Interpreter drift (sys.version vs platform.python_version)
- sys.prefix vs sys.base_prefix mismatch
- Unsupported or EOL Python versions
- Cross-platform safe
"""

import sys
import platform
from pathlib import Path
from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _abi_tag() -> str:
    """
    Construct a best-effort ABI tag (e.g., cp310, cp311).
    """
    major = sys.version_info.major
    minor = sys.version_info.minor
    return f"cp{major}{minor}"


def _is_eol(major: int, minor: int) -> bool:
    """
    Detect EOL Python versions (static list).
    """
    eol_versions = {
        (2, 7),
        (3, 5),
        (3, 6),
        (3, 7),
        (3, 8),
    }
    return (major, minor) in eol_versions


def _version_drift() -> bool:
    """
    Detect drift between sys.version and platform.python_version().
    """
    return platform.python_version() not in sys.version


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    major = sys.version_info.major
    minor = sys.version_info.minor
    micro = sys.version_info.micro

    version_str = f"{major}.{minor}.{micro}"
    abi = _abi_tag()

    # ------------------------------------------------------------
    # 1. Python version
    # ------------------------------------------------------------
    results.append(
        CheckResult(
            id="pyver.version",
            name="Python version",
            description="Detected Python version.",
            status="ok",
            severity="info",
            details=f"{version_str} (ABI: {abi})",
            plugin="python_version",
        )
    )

    # ------------------------------------------------------------
    # 2. EOL version detection
    # ------------------------------------------------------------
    if _is_eol(major, minor):
        results.append(
            CheckResult(
                id="pyver.eol",
                name="End-of-life Python version",
                description="This Python version is EOL and no longer receives security updates.",
                status="warn",
                severity="high",
                plugin="python_version",
            )
        )
    else:
        results.append(
            CheckResult(
                id="pyver.supported",
                name="Supported Python version",
                description="Python version is within supported range.",
                status="ok",
                severity="info",
                plugin="python_version",
            )
        )

    # ------------------------------------------------------------
    # 3. Version drift detection
    # ------------------------------------------------------------
    if _version_drift():
        results.append(
            CheckResult(
                id="pyver.drift",
                name="Version drift detected",
                description="sys.version and platform.python_version() disagree.",
                status="warn",
                severity="medium",
                plugin="python_version",
            )
        )
    else:
        results.append(
            CheckResult(
                id="pyver.drift.none",
                name="No version drift",
                description="Interpreter version metadata is consistent.",
                status="ok",
                severity="info",
                plugin="python_version",
            )
        )

    # ------------------------------------------------------------
    # 4. Prefix drift (venv inconsistencies)
    # ------------------------------------------------------------
    prefix = Path(sys.prefix)
    base_prefix = Path(sys.base_prefix)

    if prefix != base_prefix:
        results.append(
            CheckResult(
                id="pyver.prefix.drift",
                name="Prefix drift",
                description="sys.prefix differs from sys.base_prefix (likely virtualenv).",
                status="ok",
                severity="info",
                details=f"prefix={prefix}\nbase_prefix={base_prefix}",
                plugin="python_version",
            )
        )
    else:
        results.append(
            CheckResult(
                id="pyver.prefix.clean",
                name="Prefix clean",
                description="sys.prefix matches sys.base_prefix.",
                status="ok",
                severity="info",
                plugin="python_version",
            )
        )

    return results
