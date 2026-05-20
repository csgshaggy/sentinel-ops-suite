"""
SuperDoctor Plugin: Runtime Limits & Resource Caps
Location: tools/plugins/runtime_limits.py

Checks:
- File descriptor limits (POSIX)
- Max user processes (POSIX)
- Stack size
- Recursion limit
- Thread count (best-effort)
- Windows fallback (limited)
- Cross-platform safe
"""

import sys
import threading
from pathlib import Path
from typing import List, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode

# POSIX-only
try:
    import resource
except Exception:
    resource = None


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _get_rlimit(name) -> Optional[str]:
    """
    Return soft/hard limits for a resource.
    """
    if resource is None:
        return None
    try:
        soft, hard = resource.getrlimit(name)
        return f"soft={soft}, hard={hard}"
    except Exception:
        return None


def _thread_count() -> int:
    """
    Best-effort thread count.
    """
    try:
        return threading.active_count()
    except Exception:
        return -1


def _stack_size() -> Optional[int]:
    """
    Return stack size (POSIX only).
    """
    if resource is None:
        return None
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
        return soft
    except Exception:
        return None


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. Recursion limit
    # ------------------------------------------------------------
    rec_limit = sys.getrecursionlimit()

    results.append(
        CheckResult(
            id="limits.recursion",
            name="Recursion limit",
            description="Python recursion limit.",
            status="ok",
            severity="info",
            details=str(rec_limit),
            plugin="runtime_limits",
        )
    )

    if rec_limit < 500:
        results.append(
            CheckResult(
                id="limits.recursion.low",
                name="Low recursion limit",
                description="Recursion limit is unusually low.",
                status="warn",
                severity="medium",
                plugin="runtime_limits",
            )
        )

    # ------------------------------------------------------------
    # 2. Thread count
    # ------------------------------------------------------------
    threads = _thread_count()

    if threads >= 0:
        results.append(
            CheckResult(
                id="limits.threads",
                name="Thread count",
                description="Active Python threads.",
                status="ok",
                severity="info",
                details=str(threads),
                plugin="runtime_limits",
            )
        )

        if threads > 200:
            results.append(
                CheckResult(
                    id="limits.threads.high",
                    name="High thread count",
                    description="Thread count is unusually high.",
                    status="warn",
                    severity="high",
                    plugin="runtime_limits",
                )
            )
    else:
        results.append(
            CheckResult(
                id="limits.threads.unknown",
                name="Thread count unavailable",
                description="Could not determine thread count.",
                status="warn",
                severity="low",
                plugin="runtime_limits",
            )
        )

    # ------------------------------------------------------------
    # 3. POSIX resource limits
    # ------------------------------------------------------------
    if resource is not None:
        # File descriptors
        fd = _get_rlimit(resource.RLIMIT_NOFILE)
        if fd:
            results.append(
                CheckResult(
                    id="limits.filedesc",
                    name="File descriptor limit",
                    description="Max open file descriptors.",
                    status="ok",
                    severity="info",
                    details=fd,
                    plugin="runtime_limits",
                )
            )

        # Max user processes
        procs = _get_rlimit(resource.RLIMIT_NPROC)
        if procs:
            results.append(
                CheckResult(
                    id="limits.processes",
                    name="Max user processes",
                    description="Process limit for current user.",
                    status="ok",
                    severity="info",
                    details=procs,
                    plugin="runtime_limits",
                )
            )

        # Stack size
        stack = _stack_size()
        if stack is not None:
            results.append(
                CheckResult(
                    id="limits.stack",
                    name="Stack size",
                    description="Process stack size limit.",
                    status="ok",
                    severity="info",
                    details=str(stack),
                    plugin="runtime_limits",
                )
            )

            if stack < 512 * 1024:  # <512 KB
                results.append(
                    CheckResult(
                        id="limits.stack.low",
                        name="Low stack size",
                        description="Stack size is unusually low.",
                        status="warn",
                        severity="medium",
                        plugin="runtime_limits",
                    )
                )
    else:
        # Windows fallback
        results.append(
            CheckResult(
                id="limits.posix.unavailable",
                name="POSIX limits unavailable",
                description="POSIX resource limits not available on this platform.",
                status="ok",
                severity="info",
                plugin="runtime_limits",
            )
        )

    return results
