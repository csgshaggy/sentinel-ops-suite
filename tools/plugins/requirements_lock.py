"""
Requirements lock plugin (sync).

Validates the presence and basic readability of dependency lock files such as:
- requirements.txt
- requirements.lock
- poetry.lock
- pipfile.lock

This plugin does NOT parse dependency graphs yet — it simply checks for
existence and accessibility, forming the foundation for future drift analysis.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Checks for presence and readability of dependency lock files.",
    "entrypoint": "run",
    "mode": "sync",
}


LOCK_FILES: List[str] = [
    "requirements.txt",
    "requirements.lock",
    "poetry.lock",
    "Pipfile.lock",
]


def _check_file(path: str) -> bool:
    """
    Returns True if the file exists and is readable.
    """
    try:
        return os.path.isfile(path) and os.access(path, os.R_OK)
    except Exception:
        return False


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous lock‑file presence check.
    """
    try:
        results = {fname: _check_file(fname) for fname in LOCK_FILES}
        found = any(results.values())

        if found:
            status = Status.OK
            message = "At least one dependency lock file is present."
        else:
            status = Status.WARN
            message = "No dependency lock files found."

        data = {
            "lock_files": results,
            "found_any": found,
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
            message=f"Requirements lock plugin failed: {exc}",
        )
