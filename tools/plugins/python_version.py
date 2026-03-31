"""
Python version plugin (sync).

Reports the active Python interpreter version and implementation details.
Useful for environment validation, reproducibility checks, and CI baselining.
"""

from __future__ import annotations

import platform
import sys
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports Python interpreter version and implementation details.",
    "entrypoint": "run",
    "mode": "sync",
}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous Python version check.
    """
    try:
        data = {
            "python_version": sys.version.split()[0],
            "full_version": sys.version,
            "implementation": platform.python_implementation(),
            "compiler": platform.python_compiler(),
            "build": platform.python_build(),
            "mode": mode.value,
            "timestamp": time.time(),
        }

        return CheckResult(
            name=PLUGIN_INFO["name"],
            status=Status.OK,
            message="Python version information retrieved successfully.",
            data=data,
        )

    except Exception as exc:
        return CheckResult.fail(
            name=PLUGIN_INFO["name"],
            message=f"Python version plugin failed: {exc}",
        )
