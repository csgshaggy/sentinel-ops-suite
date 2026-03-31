"""
Storage health plugin (sync).

Performs a basic health check on mounted filesystems:
- total, used, and free space
- percentage utilization
- detection of critically full volumes

Forms the foundation for future expansion into:
- inode exhaustion checks
- mount option validation
- per‑mountpoint policy enforcement
"""

from __future__ import annotations

import shutil
import time
from typing import Any, Dict, List

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Checks disk usage and storage health.",
    "entrypoint": "run",
    "mode": "sync",
}


# You can expand this later to enumerate all mounts dynamically.
MOUNT_POINTS: List[str] = [
    "/",
]


def _check_mount(path: str) -> Dict[str, Any]:
    """
    Returns disk usage stats for a given mount point.
    """
    try:
        usage = shutil.disk_usage(path)
        percent_used = (usage.used / usage.total) * 100

        return {
            "total_gb": usage.total / (1024**3),
            "used_gb": usage.used / (1024**3),
            "free_gb": usage.free / (1024**3),
            "percent_used": percent_used,
            "healthy": percent_used < 90,
        }
    except Exception:
        return {
            "error": True,
            "healthy": False,
        }


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous storage health check.
    """
    try:
        results = {mp: _check_mount(mp) for mp in MOUNT_POINTS}

        # Determine overall status
        any_errors = any(v.get("error") for v in results.values())
        any_critical = any(v.get("percent_used", 0) >= 95 for v in results.values())
        any_warn = any(90 <= v.get("percent_used", 0) < 95 for v in results.values())

        if any_errors:
            status = Status.FAIL
            message = "Storage check encountered errors."
        elif any_critical:
            status = Status.FAIL
            message = "Critical storage utilization detected."
        elif any_warn:
            status = Status.WARN
            message = "Storage utilization elevated."
        else:
            status = Status.OK
            message = "Storage health appears normal."

        data = {
            "mounts": results,
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
            message=f"Storage health plugin failed: {exc}",
        )
