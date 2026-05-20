"""
System limits plugin (sync).

Reports OS-level resource limits such as:
- max open files (ulimit -n)
- max user processes (ulimit -u)
- core file size
- file size limits
- stack size

Forms the foundation for future enforcement of:
- hardened limit profiles
- CI baseline comparisons
- drift detection across environments
"""

from __future__ import annotations

import resource
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports OS-level resource limits (ulimits).",
    "entrypoint": "run",
    "mode": "sync",
}


LIMITS = {
    "core_file_size": resource.RLIMIT_CORE,
    "data_segment_size": resource.RLIMIT_DATA,
    "file_size": resource.RLIMIT_FSIZE,
    "open_files": resource.RLIMIT_NOFILE,
    "stack_size": resource.RLIMIT_STACK,
    "cpu_time": resource.RLIMIT_CPU,
    "max_processes": resource.RLIMIT_NPROC,
}


def _read_limit(limit_key: str, limit_const: int) -> Dict[str, Any]:
    """
    Safely read a resource limit.
    """
    try:
        soft, hard = resource.getrlimit(limit_const)
        return {"soft": soft, "hard": hard}
    except Exception:
        return {"error": True}


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous system limits check.
    """
    try:
        results = {key: _read_limit(key, const) for key, const in LIMITS.items()}

        any_errors = any(v.get("error") for v in results.values())

        if any_errors:
            status = Status.WARN
            message = "Some system limits could not be read."
        else:
            status = Status.OK
            message = "System limits retrieved successfully."

        data = {
            "limits": results,
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
            message=f"System limits plugin failed: {exc}",
        )
