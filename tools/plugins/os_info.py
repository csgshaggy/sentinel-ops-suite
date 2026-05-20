"""
Operating system information plugin (stub).

Placeholder plugin intended for future expansion to validate OS-level
configuration, kernel parameters, distro metadata, and environment details.
Currently returns a simple OK result.
"""

from __future__ import annotations

from typing import Any, Dict

from tools.super_doctor import CheckResult
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Stub plugin for operating system information checks.",
    "entrypoint": "run",
    "mode": "sync",
}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Stubbed OS info check.
    """
    return CheckResult.ok(
        name=PLUGIN_INFO["name"],
        message="OS info stub plugin executed successfully.",
        data={"stub": True, "mode": mode.value},
    )
