"""
CPU load health check plugin (sync).

Evaluates current CPU utilization and reports a simple health status.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Checks current CPU load and reports basic health.",
    "entrypoint": "run",
    "mode": "sync",
}


def _get_cpu_load() -> float:
    """
    Return a simple CPU load metric.

    On Linux, prefer os.getloadavg() if available; otherwise, return 0.0 as a safe fallback.
    """
    if hasattr(os, "getloadavg"):
        load1, _, _ = os.getloadavg()
        return float(load1)
    return 0.0


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous CPU load check.

    Mode can be used later to adjust thresholds or sampling depth.
    """
    try:
        load = _get_cpu_load()

        # Simple heuristic thresholds; you can tune these later.
        if load < 1.0:
            status = Status.OK
            message = f"CPU load is healthy (load1={load:.2f})."
        elif load < 2.0:
            status = Status.WARN
            message = f"CPU load is elevated (load1={load:.2f})."
        else:
            status = Status.FAIL
            message = f"CPU load is high (load1={load:.2f})."

        data = {
            "load1": load,
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
            message=f"CPU load plugin failed: {exc}",
        )
