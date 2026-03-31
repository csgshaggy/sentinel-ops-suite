"""
Process health plugin (sync).

Reports:
- total process count
- top CPU-consuming processes
- top memory-consuming processes
- zombie process count
- basic process table snapshot

Forms the foundation for:
- system load diagnostics
- operator console visibility
- CI environment validation
"""

from __future__ import annotations

import time
from typing import Any, Dict, List

import psutil

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports process table health and resource usage.",
    "entrypoint": "run",
    "mode": "sync",
}


def _get_process_snapshot(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Returns a snapshot of top processes by CPU usage.
    """
    procs = []
    for proc in psutil.process_iter(
        attrs=["pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            info = proc.info
            procs.append(info)
        except Exception:
            continue

    # Sort by CPU usage descending
    procs.sort(key=lambda p: p.get("cpu_percent", 0), reverse=True)
    return procs[:limit]


def _get_memory_heavy(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Returns a snapshot of top processes by memory usage.
    """
    procs = []
    for proc in psutil.process_iter(
        attrs=["pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            info = proc.info
            procs.append(info)
        except Exception:
            continue

    # Sort by memory usage descending
    procs.sort(key=lambda p: p.get("memory_percent", 0), reverse=True)
    return procs[:limit]


def _count_zombies() -> int:
    """
    Count zombie processes.
    """
    count = 0
    for proc in psutil.process_iter(attrs=["status"]):
        try:
            if proc.info.get("status") == psutil.STATUS_ZOMBIE:
                count += 1
        except Exception:
            continue
    return count


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous process health check.
    """
    try:
        total_procs = len(psutil.pids())
        zombies = _count_zombies()
        top_cpu = _get_process_snapshot()
        top_mem = _get_memory_heavy()

        if zombies > 0:
            status = Status.WARN
            message = f"Zombie processes detected: {zombies}"
        else:
            status = Status.OK
            message = "Process table is healthy."

        data = {
            "total_processes": total_procs,
            "zombie_count": zombies,
            "top_cpu_processes": top_cpu,
            "top_memory_processes": top_mem,
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
            message=f"Process health plugin failed: {exc}",
        )
