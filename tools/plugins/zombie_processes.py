"""
Zombie processes plugin (sync).

Detects:
- zombie (defunct) processes
- orphaned processes
- counts and summaries

Forms the foundation for:
- process‑tree integrity checks
- service supervision validation
- CI baselines for expected process behavior
"""

from __future__ import annotations

import time
from typing import Any, Dict, List

import psutil

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Detects zombie and orphaned processes.",
    "entrypoint": "run",
    "mode": "sync",
}


def _detect_zombies() -> List[Dict[str, Any]]:
    """
    Returns a list of zombie (defunct) processes.
    """
    zombies = []
    for proc in psutil.process_iter(attrs=["pid", "name", "status", "ppid"]):
        try:
            info = proc.info
            if info.get("status") == psutil.STATUS_ZOMBIE:
                zombies.append(info)
        except Exception:
            continue
    return zombies


def _detect_orphans() -> List[Dict[str, Any]]:
    """
    Returns a list of orphaned processes (ppid == 1).
    """
    orphans = []
    for proc in psutil.process_iter(attrs=["pid", "name", "status", "ppid"]):
        try:
            info = proc.info
            if info.get("ppid") == 1 and info.get("status") != psutil.STATUS_ZOMBIE:
                orphans.append(info)
        except Exception:
            continue
    return orphans


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous zombie/orphan process check.
    """
    try:
        zombies = _detect_zombies()
        orphans = _detect_orphans()

        zombie_count = len(zombies)
        orphan_count = len(orphans)

        if zombie_count == 0 and orphan_count == 0:
            status = Status.OK
            message = "No zombie or orphaned processes detected."
        elif zombie_count > 0:
            status = Status.WARN
            message = f"Zombie processes detected: {zombie_count}"
        else:
            status = Status.WARN
            message = f"Orphaned processes detected: {orphan_count}"

        data = {
            "zombies": zombies,
            "zombie_count": zombie_count,
            "orphans": orphans,
            "orphan_count": orphan_count,
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
            message=f"Zombie processes plugin failed: {exc}",
        )
