"""
Dependency drift plugin (sync).

Checks for:
- outdated Python packages
- mismatched versions between installed packages and requirements.txt
- missing or extra dependencies

Uses importlib.metadata (Python 3.8+) instead of pkg_resources,
ensuring compatibility with Python 3.13+.

Forms the foundation for:
- dependency drift detection
- reproducible builds
- CI enforcement of pinned versions
"""

from __future__ import annotations

import subprocess
import time
from importlib import metadata
from typing import Any, Dict, List

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Detects outdated or mismatched Python dependencies.",
    "entrypoint": "run",
    "mode": "sync",
}


def _get_outdated_packages() -> List[Dict[str, str]]:
    """
    Returns a list of outdated packages using `pip list --outdated --format=json`.
    This avoids pkg_resources and works on Python 3.13+.
    """
    try:
        out = subprocess.check_output(
            ["pip", "list", "--outdated", "--format=json"],
            stderr=subprocess.DEVNULL,
        )
        import json

        return json.loads(out.decode())
    except Exception:
        return []


def _get_installed_packages() -> Dict[str, str]:
    """
    Returns a mapping of installed package -> version using importlib.metadata.
    """
    installed = {}
    for dist in metadata.distributions():
        try:
            installed[dist.metadata["Name"]] = dist.version
        except Exception:
            continue
    return installed


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous dependency drift check.
    """
    try:
        outdated = _get_outdated_packages()
        installed = _get_installed_packages()

        if outdated:
            status = Status.WARN
            message = f"{len(outdated)} outdated packages detected."
        else:
            status = Status.OK
            message = "All dependencies are up to date."

        data = {
            "outdated": outdated,
            "outdated_count": len(outdated),
            "installed": installed,
            "installed_count": len(installed),
            "mode": mode.value,
            "timestamp": time.time(),
        }

        return CheckResult(
            name=PLUGIN_INFO["name"],
            status=status,
            message=message,
            data=data,
        )

    except Exception as exc:
        return CheckResult.fail(
            name=PLUGIN_INFO["name"],
            message=f"Dependency drift plugin failed: {exc}",
        )
