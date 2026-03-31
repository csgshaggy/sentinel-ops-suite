"""
SuperDoctor Plugin: Disk Space & Filesystem Health
Location: tools/plugins/disk_space.py

Checks:
- Available disk space on project root volume
- Percentage free
- Low‑space warnings
- Read/write test in reports directory
- Cross‑platform (Windows + Linux)
"""

import os
from pathlib import Path
from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _get_disk_usage(path: Path):
    """
    Cross‑platform disk usage using os.statvfs (Linux/macOS) or
    shutil.disk_usage (Windows fallback).
    """
    try:
        # POSIX
        st = os.statvfs(str(path))
        total = st.f_frsize * st.f_blocks
        free = st.f_frsize * st.f_bavail
        used = total - free
        return total, used, free
    except Exception:
        # Windows fallback
        try:
            import shutil

            usage = shutil.disk_usage(str(path))
            return usage.total, usage.used, usage.free
        except Exception:
            return None, None, None


def _format_bytes(num: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.1f}{unit}"
        num /= 1024
    return f"{num:.1f}PB"


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. Disk usage on project root volume
    # ------------------------------------------------------------
    total, used, free = _get_disk_usage(project_root)

    if total is None:
        results.append(
            CheckResult(
                id="disk.unavailable",
                name="Disk usage unavailable",
                description="Could not determine disk usage for project root.",
                status="warn",
                severity="medium",
                plugin="disk_space",
            )
        )
        return results

    percent_free = (free / total) * 100 if total > 0 else 0

    results.append(
        CheckResult(
            id="disk.usage",
            name="Disk usage",
            description="Disk usage for project root volume.",
            status="ok",
            severity="info",
            details=(
                f"Total: {_format_bytes(total)}\n"
                f"Used:  {_format_bytes(used)}\n"
                f"Free:  {_format_bytes(free)} ({percent_free:.1f}% free)"
            ),
            plugin="disk_space",
        )
    )

    # ------------------------------------------------------------
    # 2. Low‑space warnings
    # ------------------------------------------------------------
    if percent_free < 5:
        results.append(
            CheckResult(
                id="disk.critically_low",
                name="Critically low disk space",
                description="Less than 5% free space remaining.",
                status="fail",
                severity="critical",
                plugin="disk_space",
            )
        )
    elif percent_free < 10:
        results.append(
            CheckResult(
                id="disk.low",
                name="Low disk space",
                description="Less than 10% free space remaining.",
                status="warn",
                severity="high",
                plugin="disk_space",
            )
        )
    elif percent_free < 20:
        results.append(
            CheckResult(
                id="disk.moderate",
                name="Moderate disk space",
                description="Less than 20% free space remaining.",
                status="warn",
                severity="medium",
                plugin="disk_space",
            )
        )
    else:
        results.append(
            CheckResult(
                id="disk.healthy",
                name="Disk space healthy",
                description="Sufficient free space available.",
                status="ok",
                severity="info",
                plugin="disk_space",
            )
        )

    # ------------------------------------------------------------
    # 3. Read/write test in reports directory
    # ------------------------------------------------------------
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    test_file = reports_dir / ".superdoctor_rw_test"

    try:
        test_file.write_text("rw-test", encoding="utf-8")
        read_back = test_file.read_text(encoding="utf-8")
        if read_back.strip() == "rw-test":
            results.append(
                CheckResult(
                    id="disk.rw_ok",
                    name="Filesystem read/write OK",
                    description="Successfully wrote and read a test file in reports/.",
                    status="ok",
                    severity="info",
                    plugin="disk_space",
                )
            )
        else:
            results.append(
                CheckResult(
                    id="disk.rw_corrupt",
                    name="Filesystem corruption suspected",
                    description="Read/write test returned unexpected data.",
                    status="fail",
                    severity="high",
                    plugin="disk_space",
                )
            )
    except Exception as exc:
        results.append(
            CheckResult(
                id="disk.rw_fail",
                name="Filesystem read/write failure",
                description="Could not write/read test file in reports/.",
                status="fail",
                severity="critical",
                details=str(exc),
                plugin="disk_space",
            )
        )
    finally:
        try:
            if test_file.exists():
                test_file.unlink()
        except Exception:
            pass

    return results
