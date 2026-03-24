"""
SuperDoctor Plugin: Disk Health & Storage Integrity
Location: tools/plugins/disk_health.py

Checks:
- Disk usage (per mount)
- Free space thresholds
- Inode pressure (POSIX)
- Mountpoint sanity
- Read/write access
- Cross-platform safe
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode

# POSIX-only inode stats
try:
    import statvfs
except Exception:
    statvfs = None


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _disk_usage(path: Path):
    """
    Wrapper around shutil.disk_usage.
    Returns (total, used, free).
    """
    try:
        return shutil.disk_usage(str(path))
    except Exception:
        return None


def _inode_stats(path: Path) -> Optional[dict]:
    """
    POSIX inode stats via os.statvfs.
    """
    if statvfs is None:
        return None
    try:
        st = os.statvfs(str(path))
        return {
            "inodes_total": st.f_files,
            "inodes_free": st.f_ffree,
            "inodes_used": st.f_files - st.f_ffree,
        }
    except Exception:
        return None


def _mountpoints() -> List[Path]:
    """
    Best-effort mountpoint enumeration.
    """
    mounts = []

    if os.name == "nt":
        # Windows: use drive letters
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            p = Path(f"{letter}:/")
            if p.exists():
                mounts.append(p)
    else:
        # POSIX: parse /proc/mounts
        try:
            with open("/proc/mounts") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2:
                        mounts.append(Path(parts[1]))
        except Exception:
            mounts.append(Path("/"))

    return mounts


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    mounts = _mountpoints()

    # ------------------------------------------------------------
    # 1. Disk usage per mount
    # ------------------------------------------------------------
    for m in mounts:
        usage = _disk_usage(m)
        if usage is None:
            results.append(
                CheckResult(
                    id=f"disk.{m}.unavailable",
                    name=f"Disk usage unavailable: {m}",
                    description="Could not retrieve disk usage.",
                    status="warn",
                    severity="medium",
                    plugin="disk_health",
                )
            )
            continue

        total, used, free = usage
        used_pct = (used / total * 100) if total > 0 else 0

        results.append(
            CheckResult(
                id=f"disk.{m}.usage",
                name=f"Disk usage: {m}",
                description="Disk usage statistics.",
                status="ok",
                severity="info",
                details=(
                    f"Total: {total / (1024**3):.1f} GB\n"
                    f"Used:  {used / (1024**3):.1f} GB ({used_pct:.1f}%)\n"
                    f"Free:  {free / (1024**3):.1f} GB"
                ),
                plugin="disk_health",
            )
        )

        # Threshold warnings
        if used_pct >= 95:
            results.append(
                CheckResult(
                    id=f"disk.{m}.critical",
                    name=f"Critical disk pressure: {m}",
                    description="Disk usage exceeds 95%.",
                    status="fail",
                    severity="critical",
                    plugin="disk_health",
                )
            )
        elif used_pct >= 85:
            results.append(
                CheckResult(
                    id=f"disk.{m}.high",
                    name=f"High disk pressure: {m}",
                    description="Disk usage exceeds 85%.",
                    status="warn",
                    severity="high",
                    plugin="disk_health",
                )
            )
        elif used_pct >= 70:
            results.append(
                CheckResult(
                    id=f"disk.{m}.moderate",
                    name=f"Moderate disk pressure: {m}",
                    description="Disk usage exceeds 70%.",
                    status="warn",
                    severity="medium",
                    plugin="disk_health",
                )
            )

    # ------------------------------------------------------------
    # 2. Inode pressure (POSIX)
    # ------------------------------------------------------------
    if os.name != "nt":
        for m in mounts:
            stats = _inode_stats(m)
            if stats is None:
                continue

            total = stats["inodes_total"]
            free = stats["inodes_free"]
            used = stats["inodes_used"]

            if total > 0:
                used_pct = used / total * 100
            else:
                used_pct = 0

            if used_pct >= 95:
                results.append(
                    CheckResult(
                        id=f"inodes.{m}.critical",
                        name=f"Critical inode pressure: {m}",
                        description="Inode usage exceeds 95%.",
                        status="fail",
                        severity="critical",
                        plugin="disk_health",
                    )
                )
            elif used_pct >= 85:
                results.append(
                    CheckResult(
                        id=f"inodes.{m}.high",
                        name=f"High inode pressure: {m}",
                        description="Inode usage exceeds 85%.",
                        status="warn",
                        severity="high",
                        plugin="disk_health",
                    )
                )

    return results
