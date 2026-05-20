"""
Makefile health plugin (stub).

Intended for future validation of Makefile structure, required targets,
dependency chains, phony declarations, and CI‑enforced rules.
Currently implemented as a safe placeholder.
"""

from __future__ import annotations

from typing import Any, Dict

from tools.super_doctor import CheckResult
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Stub plugin for Makefile structure and health checks.",
    "entrypoint": "run",
    "mode": "sync",
}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Stubbed Makefile health check.
    """
    return CheckResult.ok(
        name=PLUGIN_INFO["name"],
        message="Makefile health stub plugin executed successfully.",
        data={"stub": True, "mode": mode.value},
    )
