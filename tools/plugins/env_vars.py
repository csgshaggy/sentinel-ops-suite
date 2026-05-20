"""
Environment variables plugin (stub).

Placeholder plugin that simply reports that it executed successfully.
Real logic can be added later to validate required environment variables,
check for missing secrets, or detect misconfigurations.
"""

from __future__ import annotations

from typing import Any, Dict

from tools.super_doctor import CheckResult
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Stub plugin for environment variable checks.",
    "entrypoint": "run",
    "mode": "sync",
}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Stubbed environment variable check.
    """
    return CheckResult.ok(
        name=PLUGIN_INFO["name"],
        message="Environment variable stub plugin executed successfully.",
        data={"stub": True, "mode": mode.value},
    )
