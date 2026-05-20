"""
Kernel information plugin (sync).

Reports basic kernel details such as version, release, and machine type.
Useful for environment diagnostics and baseline system profiling.
"""

from __future__ import annotations

import platform
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports kernel version and platform information.",
    "entrypoint": "run",
    "mode": "sync",
}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous kernel information check.
    """
    try:
        data = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "mode": mode.value,
            "timestamp": time.time(),
        }

        return CheckResult(
            name=PLUGIN_INFO["name"],
            status=Status.OK,
            message="Kernel information retrieved successfully.",
            data=data,
        )

    except Exception as exc:
        return CheckResult.fail(
            name=PLUGIN_INFO["name"],
            message=f"Kernel info plugin failed: {exc}",
        )
