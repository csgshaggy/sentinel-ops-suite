"""
Disk space health check plugin (sync).

Reports available disk space and simple health thresholds.
"""

from __future__ import annotations

import shutil
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Checks free disk space and reports health.",
    "entrypoint": "run",
    "mode": "sync",
}


def _get_disk_usage(path: str = "/") -> Dict[str, float]:
    """
    Return disk usage statistics for the given path.
    Values returned in gigabytes.
    """
    usage = shutil.disk_usage(path)
    gb = 1024 * 1024 * 1024

    return {
        "total_gb": usage.total / gb,
        "used_gb": usage.used / gb,
        "free_gb": usage.free / gb,
        "percent_used": (usage.used / usage.total) * 100,
    }


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous disk space check.
    """
    try:
        stats = _get_disk_usage("/")

        percent = stats["percent_used"]

        if percent < 70:
            status = Status.OK
            message = f"Disk usage healthy ({percent:.1f}% used)."
        elif percent < 90:
            status = Status.WARN
            message = f"Disk usage elevated ({percent:.1f}% used)."
        else:
            status = Status.FAIL
            message = f"Disk usage critical ({percent:.1f}% used)."

        stats["mode"] = mode.value
        stats["timestamp"] = time.time()

        return CheckResult(
            name=PLUGIN_INFO["name"],
            status=status,
            message=message,
            data=stats,
        )

    except Exception as exc:
        return CheckResult.fail(
            name=PLUGIN_INFO["name"],
            message=f"Disk space plugin failed: {exc}",
        )
