"""
Package integrity plugin (sync).

Checks for:
- missing packages listed in requirements.txt
- extra packages installed but not listed
- version mismatches between installed packages and requirements.txt

Uses importlib.metadata (Python 3.8+) for compatibility with Python 3.13+.

Forms the foundation for:
- reproducible builds
- dependency integrity enforcement
- CI validation of pinned versions
"""

from __future__ import annotations

import os
import time
from importlib import metadata
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Validates installed packages against requirements.txt.",
    "entrypoint": "run",
    "mode": "sync",
}


def _load_requirements() -> Dict[str, str]:
    """
    Parse requirements.txt into {package: version}.
    """
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        return {}

    reqs = {}
    with open(req_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "==" not in line:
                continue
            pkg, ver = line.split("==", 1)
            reqs[pkg.strip()] = ver.strip()

    return reqs


def _get_installed() -> Dict[str, str]:
    """
    Returns installed packages using importlib.metadata.
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
    Synchronous package integrity check.
    """
    try:
        required = _load_requirements()
        installed = _get_installed()

        missing = []
        mismatched = []
        extra = []

        # Check for missing or mismatched versions
        for pkg, req_ver in required.items():
            inst_ver = installed.get(pkg)
            if inst_ver is None:
                missing.append(pkg)
            elif inst_ver != req_ver:
                mismatched.append(
                    {"package": pkg, "required": req_ver, "installed": inst_ver}
                )

        # Check for extra packages
        for pkg in installed:
            if pkg not in required:
                extra.append(pkg)

        if missing or mismatched:
            status = Status.WARN
            message = "Package integrity issues detected."
        else:
            status = Status.OK
            message = "Package integrity is clean."

        data = {
            "required_count": len(required),
            "installed_count": len(installed),
            "missing": missing,
            "missing_count": len(missing),
            "mismatched": mismatched,
            "mismatched_count": len(mismatched),
            "extra": extra,
            "extra_count": len(extra),
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
            message=f"Package integrity plugin failed: {exc}",
        )
