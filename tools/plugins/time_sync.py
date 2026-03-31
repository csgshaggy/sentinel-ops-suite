"""
Time synchronization plugin (sync).

Checks:
- current system time
- drift between system time and monotonic clock
- presence of NTP or chrony services (lightweight check)
- basic sanity validation for timekeeping

Forms the foundation for:
- strict CI timestamp validation
- distributed system drift detection
- audit‑grade time consistency checks
"""

from __future__ import annotations

import subprocess
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Checks system time synchronization and drift indicators.",
    "entrypoint": "run",
    "mode": "sync",
}


def _run_cmd(cmd: list[str]) -> str:
    """
    Safely run a command and return stdout as text.
    """
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return ""


def _check_ntp_status() -> str:
    """
    Returns a lightweight indicator of NTP/chrony status.
    """
    # Try chrony first
    out = _run_cmd(["chronyc", "tracking"])
    if out:
        return "chrony"

    # Try systemd-timesyncd
    out = _run_cmd(["timedatectl", "show"])
    if "NTPSynchronized=" in out:
        return "systemd-timesyncd"

    # Try ntpd
    out = _run_cmd(["ntpq", "-pn"])
    if out:
        return "ntpd"

    return "unknown"


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous time synchronization check.
    """
    try:
        now = time.time()
        monotonic_now = time.monotonic()
        drift = abs(now - monotonic_now)

        ntp_status = _check_ntp_status()

        # Drift thresholds are intentionally loose — this is a baseline check.
        if drift < 5:
            status = Status.OK
            message = "Time synchronization appears normal."
        else:
            status = Status.WARN
            message = f"Clock drift detected ({drift:.2f}s)."

        data = {
            "system_time": now,
            "monotonic_time": monotonic_now,
            "drift_seconds": drift,
            "ntp_provider": ntp_status,
            "mode": mode.value,
            "timestamp": now,
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
            message=f"Time synchronization plugin failed: {exc}",
        )
