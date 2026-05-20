"""
Logging configuration plugin (stub).

Placeholder plugin intended for future validation of logging settings,
log rotation policies, handler configuration, and formatting rules.
Currently returns a simple OK result.
"""

from __future__ import annotations

from typing import Any, Dict

from tools.super_doctor import CheckResult
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Stub plugin for logging configuration checks.",
    "entrypoint": "run",
    "mode": "sync",
}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Stubbed logging configuration check.
    """
    return CheckResult.ok(
        name=PLUGIN_INFO["name"],
        message="Logging configuration stub plugin executed successfully.",
        data={"stub": True, "mode": mode.value},
    )
