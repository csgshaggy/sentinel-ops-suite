"""
SuperDoctor Plugin: File System Integrity
Location: tools/plugins/file_system.py

Checks:
- Unreadable directories
- Unreadable files
- Symlink loops (best-effort)
- Suspicious permissions (world-writable, no read bit)
- Path traversal hazards
- Cross-platform safe
"""

import os
import stat
from pathlib import Path
from typing import List, Set

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _is_world_writable(path: Path) -> bool:
    try:
        mode = path.stat().st_mode
        return bool(mode & stat.S_IWOTH)
    except Exception:
        return False


def _is_readable(path: Path) -> bool:
    try:
        return os.access(path, os.R_OK)
    except Exception:
        return False


def _detect_symlink_loops(root: Path) -> List[str]:
    """
    Best-effort symlink loop detection.
    Tracks visited inodes to detect cycles.
    """
    visited: Set[int] = set()
    loops = []

    for p in root.rglob("*"):
        try:
            if p.is_symlink():
                target = p.resolve()
                inode = target.stat().st_ino
                if inode in visited:
                    loops.append(str(p))
                else:
                    visited.add(inode)
        except Exception:
            continue

    return loops


def _detect_unreadable(root: Path) -> (List[str], List[str]):
    unreadable_dirs = []
    unreadable_files = []

    for p in root.rglob("*"):
        try:
            if p.is_dir():
                if not _is_readable(p):
                    unreadable_dirs.append(str(p.relative_to(root)))
            elif p.is_file():
                if not _is_readable(p):
                    unreadable_files.append(str(p.relative_to(root)))
        except Exception:
            continue

    return unreadable_dirs, unreadable_files


def _detect_permission_anomalies(root: Path) -> List[str]:
    anomalies = []

    for p in root.rglob("*"):
        try:
            mode = p.stat().st_mode

            # World-writable
            if mode & stat.S_IWOTH:
                anomalies.append(f"{p.relative_to(root)} (world-writable)")

            # No read bit for owner
            if not (mode & stat.S_IRUSR):
                anomalies.append(f"{p.relative_to(root)} (owner cannot read)")
        except Exception:
            continue

    return anomalies


def _detect_path_traversal(root: Path) -> List[str]:
    """
    Detect files with names that could be used for traversal attacks.
    """
    suspicious = []
    for p in root.rglob("*"):
        name = p.name
        if ".." in name or name.startswith(("/", "\\")):
            suspicious.append(str(p.relative_to(root)))
    return suspicious


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. Unreadable directories/files
    # ------------------------------------------------------------
    unread_dirs, unread_files = _detect_unreadable(project_root)

    if unread_dirs or unread_files:
        details = []
        if unread_dirs:
            details.append("Unreadable directories:\n" + "\n".join(unread_dirs))
        if unread_files:
            details.append("Unreadable files:\n" + "\n".join(unread_files))

        results.append(
            CheckResult(
                id="fs.unreadable",
                name="Unreadable filesystem entries",
                description="Some files or directories cannot be read.",
                status="warn",
                severity="medium",
                details="\n\n".join(details),
                plugin="file_system",
            )
        )
    else:
        results.append(
            CheckResult(
                id="fs.unreadable.none",
                name="All files readable",
                description="No unreadable files or directories detected.",
                status="ok",
                severity="info",
                plugin="file_system",
            )
        )

    # ------------------------------------------------------------
    # 2. Symlink loops
    # ------------------------------------------------------------
    loops = _detect_symlink_loops(project_root)

    if loops:
        results.append(
            CheckResult(
                id="fs.symlink_loops",
                name="Symlink loops detected",
                description="Potential symlink loops found.",
                status="warn",
                severity="high",
                details="\n".join(loops),
                plugin="file_system",
            )
        )
    else:
        results.append(
            CheckResult(
                id="fs.symlink_loops.none",
                name="No symlink loops",
                description="No symlink loops detected.",
                status="ok",
                severity="info",
                plugin="file_system",
            )
        )

    # ------------------------------------------------------------
    # 3. Permission anomalies
    # ------------------------------------------------------------
    anomalies = _detect_permission_anomalies(project_root)

    if anomalies:
        results.append(
            CheckResult(
                id="fs.permissions",
                name="Permission anomalies",
                description="Suspicious file permissions detected.",
                status="warn",
                severity="medium",
                details="\n".join(anomalies),
                plugin="file_system",
            )
        )
    else:
        results.append(
            CheckResult(
                id="fs.permissions.none",
                name="Permissions normal",
                description="No suspicious file permissions detected.",
                status="ok",
                severity="info",
                plugin="file_system",
            )
        )

    # ------------------------------------------------------------
    # 4. Path traversal hazards
    # ------------------------------------------------------------
    traversal = _detect_path_traversal(project_root)

    if traversal:
        results.append(
            CheckResult(
                id="fs.traversal",
                name="Path traversal hazards",
                description="Files with suspicious names detected.",
                status="warn",
                severity="medium",
                details="\n".join(traversal),
                plugin="file_system",
            )
        )
    else:
        results.append(
            CheckResult(
                id="fs.traversal.none",
                name="No traversal hazards",
                description="No suspicious filenames detected.",
                status="ok",
                severity="info",
                plugin="file_system",
            )
        )

    return results
