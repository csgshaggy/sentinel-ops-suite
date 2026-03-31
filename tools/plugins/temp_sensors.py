"""
Temperature sensors plugin (sync).

Reports system temperature readings when available:
- CPU temperature sensors
- Other thermal zones exposed by the OS

Forms the foundation for:
- thermal throttling detection
- hardware degradation alerts
- CI‑based thermal baselining
"""

from __future__ import annotations

import time
from typing import Any, Dict

import psutil

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports system temperature sensor readings.",
    "entrypoint": "run",
    "mode": "sync",
}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous temperature sensor check.
    """
    try:
        temps = psutil.sensors_temperatures(fahrenheit=False) or {}

        if not temps:
            status = Status.WARN
            message = "No temperature sensors detected."
        else:
            status = Status.OK
            message = "Temperature sensor data retrieved."

        data = {
            "sensors": temps,
            "sensor_count": sum(len(v) for v in temps.values()),
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
            message=f"Temperature sensors plugin failed: {exc}",
        )
