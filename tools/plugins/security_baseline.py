"""
Security baseline plugin (sync).

Performs lightweight baseline security checks such as:
- whether the user is running as root
- basic umask value
- presence of common sensitive world-readable files
- simple environment hardening indicators

This is intentionally minimal and non-invasive, forming the foundation
for future expansion into a full security posture assessment.
"""

from __future__ import annotations

import os
import stat
import time
from typing import Any, Dict, List

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Performs lightweight baseline security checks.",
    "entrypoint": "run",
    "mode": "sync",
}


SENSITIVE_PATHS: List[str] = [
    "/etc/shadow",
    "/etc/passwd",
    "/root",
]


def _is_world_readable(path: str) -> bool:
    """
    Returns True if the file exists and is world-readable.
    """
    try:
        st = os.stat(path)
        return bool(st.st_mode & stat.S_IROTH)
    except Exception:
        return False


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous security baseline check.
    """
    try:
        is_root = os.geteuid() == 0 if hasattr(os, "geteuid") else False
        umask_val = os.umask(0)
        os.umask(umask_val)  # restore

        world_readable = {path: _is_world_readable(path) for path in SENSITIVE_PATHS}

        flagged = any(world_readable.values())

        if not flagged and not is_root:
            status = Status.OK
            message = "Security baseline appears healthy."
        elif flagged:
            status = Status.WARN
            message = "Potentially sensitive world-readable files detected."
        else:
            status = Status.WARN
            message = "Running as root — baseline security elevated risk."

        data = {
            "is_root": is_root,
            "umask": oct(umask_val),
            "world_readable_sensitive": world_readable,
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
            message=f"Security baseline plugin failed: {exc}",
        )
