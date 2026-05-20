"""
System uptime plugin (sync).

Reports:
- total system uptime (seconds)
- human‑readable uptime
- boot timestamp

Forms the foundation for:
- uptime policy enforcement
- reboot‑required detection
- drift analysis across nodes
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Dict

import psutil

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports system uptime and boot timestamp.",
    "entrypoint": "run",
    "mode": "sync",
}


def _format_duration(seconds: float) -> str:
    """
    Convert seconds into a human‑readable duration.
    """
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")

    if not parts:
        parts.append(f"{int(seconds)}s")

    return " ".join(parts)


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous system uptime check.
    """
    try:
        boot_ts = psutil.boot_time()
        now = time.time()
        uptime_seconds = now - boot_ts

        data = {
            "uptime_seconds": uptime_seconds,
            "uptime_human": _format_duration(uptime_seconds),
            "boot_timestamp": boot_ts,
            "boot_iso": datetime.fromtimestamp(boot_ts).isoformat(),
            "mode": mode.value,
            "timestamp": now,
        }

        return CheckResult(
            name=PLUGIN_INFO["name"],
            status=Status.OK,
            message="System uptime retrieved successfully.",
            data=data,
        )

    except Exception as exc:
        return CheckResult.fail(
            name=PLUGIN_INFO["name"],
            message=f"System uptime plugin failed: {exc}",
        )
