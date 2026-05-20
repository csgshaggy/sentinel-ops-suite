"""
Network health plugin (sync).

Reports:
- active network interfaces
- IP addresses (IPv4/IPv6)
- interface state (UP/DOWN)
- basic connectivity check (ping to 8.8.8.8)
- RX/TX statistics

Forms the foundation for:
- network diagnostics
- operator console visibility
- CI environment validation
"""

from __future__ import annotations

import subprocess
import time
from typing import Any, Dict, List

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports network interface status and connectivity.",
    "entrypoint": "run",
    "mode": "sync",
}


def _run(cmd: List[str]) -> str:
    """
    Safely run a command and return stdout as text.
    """
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return ""


def _get_interfaces() -> List[Dict[str, Any]]:
    """
    Parse `ip -j addr` for interface info.
    """
    try:
        out = _run(["ip", "-j", "addr"])
        if not out:
            return []

        import json

        data = json.loads(out)
        interfaces = []

        for iface in data:
            interfaces.append(
                {
                    "name": iface.get("ifname"),
                    "state": iface.get("operstate"),
                    "addresses": [
                        addr.get("local")
                        for addr in iface.get("addr_info", [])
                        if "local" in addr
                    ],
                }
            )

        return interfaces

    except Exception:
        return []


def _ping_test() -> bool:
    """
    Basic connectivity test to 8.8.8.8.
    """
    try:
        subprocess.check_output(
            ["ping", "-c", "1", "-W", "1", "8.8.8.8"],
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous network health check.
    """
    try:
        interfaces = _get_interfaces()
        connectivity = _ping_test()

        if not interfaces:
            status = Status.WARN
            message = "No network interfaces detected."
        elif not connectivity:
            status = Status.WARN
            message = "Network interfaces present but no connectivity."
        else:
            status = Status.OK
            message = "Network connectivity is healthy."

        data = {
            "interfaces": interfaces,
            "interface_count": len(interfaces),
            "connectivity": connectivity,
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
            message=f"Network health plugin failed: {exc}",
        )
