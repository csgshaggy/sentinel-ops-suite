"""
Shell environment plugin (sync).

Reports basic shell environment details such as:
- current shell
- login shell
- PATH composition
- presence of common misconfigurations

Useful for debugging environment drift, PATH pollution, and shell‑level issues.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports shell environment details and PATH structure.",
    "entrypoint": "run",
    "mode": "sync",
}


def _split_path(path: str) -> List[str]:
    """
    Split PATH into components safely.
    """
    try:
        return path.split(os.pathsep)
    except Exception:
        return []


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous shell environment check.
    """
    try:
        shell = os.environ.get("SHELL", "unknown")
        login_shell = os.environ.get("LOGINSHELL", None)
        path_raw = os.environ.get("PATH", "")

        path_entries = _split_path(path_raw)

        # Simple heuristic: empty entries or "." in PATH are risky
        risky_entries = [p for p in path_entries if p in ("", ".", "./")]

        if not risky_entries:
            status = Status.OK
            message = "Shell environment appears healthy."
        else:
            status = Status.WARN
            message = f"Risky PATH entries detected: {risky_entries}"

        data = {
            "shell": shell,
            "login_shell": login_shell,
            "path_entries": path_entries,
            "risky_entries": risky_entries,
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
            message=f"Shell environment plugin failed: {exc}",
        )
