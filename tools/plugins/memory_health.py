"""
Memory health check plugin (sync).

Reports system memory usage and evaluates basic health thresholds.
"""

from __future__ import annotations

import time
from typing import Any, Dict

import psutil

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Checks system memory usage and reports health.",
    "entrypoint": "run",
    "mode": "sync",
}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous memory health check.
    """
    try:
        mem = psutil.virtual_memory()

        percent = mem.percent

        if percent < 70:
            status = Status.OK
            message = f"Memory usage healthy ({percent:.1f}% used)."
        elif percent < 90:
            status = Status.WARN
            message = f"Memory usage elevated ({percent:.1f}% used)."
        else:
            status = Status.FAIL
            message = f"Memory usage critical ({percent:.1f}% used)."

        data = {
            "total_gb": mem.total / (1024**3),
            "available_gb": mem.available / (1024**3),
            "used_gb": mem.used / (1024**3),
            "percent_used": percent,
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
            message=f"Memory health plugin failed: {exc}",
        )
