"""
System services plugin (sync).

Performs a lightweight check of systemd services:
- identifies failed services
- identifies services in degraded state
- reports total active vs. inactive units

This forms the foundation for future expansion into:
- service dependency graph validation
- drift detection
- policy enforcement for required services
"""

from __future__ import annotations

import subprocess
import time
from typing import Any, Dict, List

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Checks systemd service health and failure states.",
    "entrypoint": "run",
    "mode": "sync",
}


def _run_cmd(cmd: List[str]) -> str:
    """
    Safely run a command and return stdout as text.
    """
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return ""


def _list_failed_services() -> List[str]:
    """
    Returns a list of failed systemd services.
    """
    output = _run_cmd(["systemctl", "--failed", "--no-legend", "--plain"])
    if not output:
        return []

    lines = [line.strip() for line in output.splitlines() if line.strip()]
    services = [line.split()[0] for line in lines if line]
    return services


def _system_state() -> str:
    """
    Returns the systemd overall state (e.g., 'running', 'degraded').
    """
    return _run_cmd(["systemctl", "is-system-running"]) or "unknown"


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous system services check.
    """
    try:
        failed = _list_failed_services()
        state = _system_state()

        if state == "running" and not failed:
            status = Status.OK
            message = "System services appear healthy."
        elif state == "degraded" or failed:
            status = Status.WARN
            message = "Some system services are degraded or failed."
        else:
            status = Status.WARN
            message = f"System state: {state}"

        data = {
            "system_state": state,
            "failed_services": failed,
            "failed_count": len(failed),
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
            message=f"System services plugin failed: {exc}",
        )
