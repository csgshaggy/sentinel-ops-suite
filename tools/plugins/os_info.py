"""
SuperDoctor Plugin: Operating System & Platform Info
Location: tools/plugins/os_info.py

Checks:
- OS name and version
- Kernel version (Linux) / Windows build
- Architecture (x86_64, ARM64, etc.)
- Python platform tags
- Environment characteristics (WSL, container hints)
- PATH sanity
"""

import os
import platform
from pathlib import Path
from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode


def _detect_wsl() -> bool:
    """
    Detect Windows Subsystem for Linux.
    """
    try:
        with open("/proc/version", "r") as f:
            text = f.read().lower()
            return "microsoft" in text or "wsl" in text
    except Exception:
        return False


def _detect_container() -> bool:
    """
    Detect containerized environments (best-effort).
    """
    # Docker / containerd markers
    if Path("/.dockerenv").exists():
        return True

    try:
        with open("/proc/1/cgroup", "r") as f:
            text = f.read().lower()
            if "docker" in text or "containerd" in text or "kubepods" in text:
                return True
    except Exception:
        pass

    return False


def _path_sanity() -> List[str]:
    """
    Detect PATH entries that do not exist.
    """
    bad = []
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if entry and not Path(entry).exists():
            bad.append(entry)
    return bad


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. OS name and version
    # ------------------------------------------------------------
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()

    results.append(
        CheckResult(
            id="os.info",
            name="Operating system info",
            description="Detected OS name and version.",
            status="ok",
            severity="info",
            details=f"{os_name} {os_release} (version: {os_version})",
            plugin="os_info",
        )
    )

    # ------------------------------------------------------------
    # 2. Architecture
    # ------------------------------------------------------------
    arch = platform.machine()

    results.append(
        CheckResult(
            id="os.arch",
            name="CPU architecture",
            description="Detected system architecture.",
            status="ok",
            severity="info",
            details=arch,
            plugin="os_info",
        )
    )

    # ------------------------------------------------------------
    # 3. Python platform tags
    # ------------------------------------------------------------
    impl = platform.python_implementation()
    py_ver = platform.python_version()

    results.append(
        CheckResult(
            id="os.python_platform",
            name="Python platform details",
            description="Python implementation and version.",
            status="ok",
            severity="info",
            details=f"{impl} {py_ver}",
            plugin="os_info",
        )
    )

    # ------------------------------------------------------------
    # 4. WSL detection
    # ------------------------------------------------------------
    if _detect_wsl():
        results.append(
            CheckResult(
                id="os.wsl",
                name="WSL environment detected",
                description="Running inside Windows Subsystem for Linux.",
                status="warn",
                severity="medium",
                plugin="os_info",
            )
        )
    else:
        results.append(
            CheckResult(
                id="os.wsl.none",
                name="Not running in WSL",
                description="No WSL indicators detected.",
                status="ok",
                severity="info",
                plugin="os_info",
            )
        )

    # ------------------------------------------------------------
    # 5. Container detection
    # ------------------------------------------------------------
    if _detect_container():
        results.append(
            CheckResult(
                id="os.container",
                name="Container environment detected",
                description="Running inside a container (Docker/Kubernetes/etc.).",
                status="warn",
                severity="medium",
                plugin="os_info",
            )
        )
    else:
        results.append(
            CheckResult(
                id="os.container.none",
                name="Not running in a container",
                description="No container indicators detected.",
                status="ok",
                severity="info",
                plugin="os_info",
            )
        )

    # ------------------------------------------------------------
    # 6. PATH sanity
    # ------------------------------------------------------------
    bad_paths = _path_sanity()

    if bad_paths:
        results.append(
            CheckResult(
                id="os.path.bad_entries",
                name="Invalid PATH entries",
                description="Some PATH entries do not exist.",
                status="warn",
                severity="low",
                details="\n".join(bad_paths),
                plugin="os_info",
            )
        )
    else:
        results.append(
            CheckResult(
                id="os.path.ok",
                name="PATH entries valid",
                description="All PATH entries exist.",
                status="ok",
                severity="info",
                plugin="os_info",
            )
        )

    return results
