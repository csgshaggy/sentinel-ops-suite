"""
SuperDoctor Plugin: Baseline Security & Environment Sanity
Location: tools/plugins/security_basics.py

Checks:
- Umask sanity
- World-writable directories in project tree
- Unsafe environment variables
- SSH agent sanity
- PATH poisoning risks
- Cross-platform safe
"""

import os
import stat
from pathlib import Path
from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

UNSAFE_ENV_VARS = [
    "LD_PRELOAD",
    "LD_LIBRARY_PATH",
    "PYTHONPATH",
    "DYLD_INSERT_LIBRARIES",
]


def _umask_value() -> int:
    """
    Retrieve current umask without modifying it.
    """
    old = os.umask(0)
    os.umask(old)
    return old


def _world_writable_dirs(root: Path) -> List[str]:
    """
    Detect world-writable directories under project root.
    """
    ww = []
    for p in root.rglob("*"):
        try:
            if p.is_dir():
                mode = p.stat().st_mode
                if mode & stat.S_IWOTH:
                    ww.append(str(p.relative_to(root)))
        except Exception:
            continue
    return ww


def _unsafe_env() -> List[str]:
    """
    Detect unsafe environment variables that are set.
    """
    found = []
    for var in UNSAFE_ENV_VARS:
        if var in os.environ:
            found.append(f"{var}={os.environ.get(var)}")
    return found


def _ssh_agent_sanity() -> List[str]:
    """
    Detect SSH agent anomalies.
    """
    issues = []
    sock = os.environ.get("SSH_AUTH_SOCK")
    pid = os.environ.get("SSH_AGENT_PID")

    if sock and not Path(sock).exists():
        issues.append(f"SSH_AUTH_SOCK points to missing socket: {sock}")

    if pid and not pid.isdigit():
        issues.append(f"SSH_AGENT_PID is not numeric: {pid}")

    return issues


def _path_poisoning() -> List[str]:
    """
    Detect PATH entries that are dangerous:
    - empty entries
    - current directory
    - non-existent directories
    """
    issues = []
    path = os.environ.get("PATH", "")
    for entry in path.split(os.pathsep):
        if entry == "":
            issues.append("Empty PATH entry")
        elif entry == ".":
            issues.append("PATH contains '.' (current directory)")
        elif not Path(entry).exists():
            issues.append(f"Nonexistent PATH entry: {entry}")
    return issues


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. Umask sanity
    # ------------------------------------------------------------
    um = _umask_value()

    if um > 0o077:
        results.append(
            CheckResult(
                id="sec.umask.weak",
                name="Weak umask",
                description="Umask is too permissive.",
                status="warn",
                severity="medium",
                details=oct(um),
                plugin="security_basics",
            )
        )
    else:
        results.append(
            CheckResult(
                id="sec.umask.ok",
                name="Umask OK",
                description="Umask is appropriately restrictive.",
                status="ok",
                severity="info",
                details=oct(um),
                plugin="security_basics",
            )
        )

    # ------------------------------------------------------------
    # 2. World-writable directories
    # ------------------------------------------------------------
    ww = _world_writable_dirs(project_root)

    if ww:
        results.append(
            CheckResult(
                id="sec.world_writable",
                name="World-writable directories",
                description="Some directories are world-writable.",
                status="warn",
                severity="high",
                details="\n".join(ww),
                plugin="security_basics",
            )
        )
    else:
        results.append(
            CheckResult(
                id="sec.world_writable.none",
                name="No world-writable directories",
                description="No world-writable directories detected.",
                status="ok",
                severity="info",
                plugin="security_basics",
            )
        )

    # ------------------------------------------------------------
    # 3. Unsafe environment variables
    # ------------------------------------------------------------
    unsafe = _unsafe_env()

    if unsafe:
        results.append(
            CheckResult(
                id="sec.env.unsafe",
                name="Unsafe environment variables",
                description="Potentially dangerous environment variables are set.",
                status="warn",
                severity="medium",
                details="\n".join(unsafe),
                plugin="security_basics",
            )
        )
    else:
        results.append(
            CheckResult(
                id="sec.env.ok",
                name="Environment variables OK",
                description="No unsafe environment variables detected.",
                status="ok",
                severity="info",
                plugin="security_basics",
            )
        )

    # ------------------------------------------------------------
    # 4. SSH agent sanity
    # ------------------------------------------------------------
    ssh = _ssh_agent_sanity()

    if ssh:
        results.append(
            CheckResult(
                id="sec.ssh.agent",
                name="SSH agent anomalies",
                description="SSH agent environment variables appear inconsistent.",
                status="warn",
                severity="low",
                details="\n".join(ssh),
                plugin="security_basics",
            )
        )
    else:
        results.append(
            CheckResult(
                id="sec.ssh.ok",
                name="SSH agent OK",
                description="SSH agent environment appears normal.",
                status="ok",
                severity="info",
                plugin="security_basics",
            )
        )

    # ------------------------------------------------------------
    # 5. PATH poisoning
    # ------------------------------------------------------------
    path_issues = _path_poisoning()

    if path_issues:
        results.append(
            CheckResult(
                id="sec.path.poison",
                name="PATH poisoning risks",
                description="Potentially dangerous PATH entries detected.",
                status="warn",
                severity="medium",
                details="\n".join(path_issues),
                plugin="security_basics",
            )
        )
    else:
        results.append(
            CheckResult(
                id="sec.path.ok",
                name="PATH OK",
                description="PATH entries appear safe.",
                status="ok",
                severity="info",
                plugin="security_basics",
            )
        )

    return results
