"""
OS release plugin (stub).

Placeholder plugin intended for future expansion to validate distribution
release metadata, kernel release alignment, and OS‑level configuration drift.
Currently implemented as a simple stub.
"""

from __future__ import annotations

from typing import Any, Dict

from tools.super_doctor import CheckResult
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Stub plugin for OS release metadata checks.",
    "entrypoint": "run",
    "mode": "sync",
}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Stubbed OS release check.
    """
    return CheckResult.ok(
        name=PLUGIN_INFO["name"],
        message="OS release stub plugin executed successfully.",
        data={"stub": True, "mode": mode.value},
    )
