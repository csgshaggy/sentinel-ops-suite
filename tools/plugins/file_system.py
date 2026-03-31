"""
File system health check plugin (sync).

Performs basic checks on filesystem responsiveness and directory accessibility.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Checks basic filesystem accessibility and responsiveness.",
    "entrypoint": "run",
    "mode": "sync",
}


def _check_access(path: str) -> bool:
    """
    Returns True if the path exists and is accessible.
    """
    try:
        return os.path.exists(path) and os.access(path, os.R_OK)
    except Exception:
        return False


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous filesystem health check.
    """
    try:
        root_ok = _check_access("/")
        home_ok = _check_access(os.path.expanduser("~"))
        tmp_ok = _check_access("/tmp")

        # Simple scoring
        score = sum([root_ok, home_ok, tmp_ok])

        if score == 3:
            status = Status.OK
            message = "Filesystem paths are accessible."
        elif score == 2:
            status = Status.WARN
            message = "Some filesystem paths are not accessible."
        else:
            status = Status.FAIL
            message = "Critical filesystem paths are inaccessible."

        data = {
            "root_accessible": root_ok,
            "home_accessible": home_ok,
            "tmp_accessible": tmp_ok,
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
            message=f"Filesystem plugin failed: {exc}",
        )
