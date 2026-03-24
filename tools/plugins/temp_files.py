"""
SuperDoctor Plugin: Temporary File & Residue Scanner
Location: tools/plugins/temp_files.py

Checks:
- Leftover temp files in project tree
- Orphaned lockfiles (.lock)
- Stale PID files
- Crash residue (.tmp, .bak, .swp, .swx)
- Large temp files
- Cross-platform safe
"""

from pathlib import Path
from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Patterns to detect
# ------------------------------------------------------------

TEMP_PATTERNS = [
    "*.tmp",
    "*.temp",
    "*.bak",
    "*.swp",
    "*.swx",
    "*.old",
]

LOCK_PATTERNS = [
    "*.lock",
]

PID_PATTERNS = [
    "*.pid",
]


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _find_matches(root: Path, patterns: List[str]) -> List[Path]:
    matches = []
    for pattern in patterns:
        matches.extend(root.rglob(pattern))
    return matches


def _large_temp_files(paths: List[Path], threshold_mb: int = 10) -> List[str]:
    """
    Detect temp files larger than threshold.
    """
    large = []
    for p in paths:
        try:
            size_mb = p.stat().st_size / (1024 * 1024)
            if size_mb > threshold_mb:
                large.append(f"{p} ({size_mb:.1f} MB)")
        except Exception:
            continue
    return large


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. Temp files
    # ------------------------------------------------------------
    temp_files = _find_matches(project_root, TEMP_PATTERNS)

    if temp_files:
        results.append(
            CheckResult(
                id="temp.files",
                name="Temporary files detected",
                description="Leftover temporary or crash-related files found.",
                status="warn",
                severity="medium",
                details="\n".join(str(p.relative_to(project_root)) for p in temp_files),
                plugin="temp_files",
            )
        )
    else:
        results.append(
            CheckResult(
                id="temp.files.none",
                name="No temporary files",
                description="No leftover temp or crash files detected.",
                status="ok",
                severity="info",
                plugin="temp_files",
            )
        )

    # ------------------------------------------------------------
    # 2. Lockfiles
    # ------------------------------------------------------------
    lock_files = _find_matches(project_root, LOCK_PATTERNS)

    if lock_files:
        results.append(
            CheckResult(
                id="temp.lockfiles",
                name="Lockfiles detected",
                description="Orphaned lockfiles found.",
                status="warn",
                severity="medium",
                details="\n".join(str(p.relative_to(project_root)) for p in lock_files),
                plugin="temp_files",
            )
        )
    else:
        results.append(
            CheckResult(
                id="temp.lockfiles.none",
                name="No lockfiles",
                description="No orphaned lockfiles detected.",
                status="ok",
                severity="info",
                plugin="temp_files",
            )
        )

    # ------------------------------------------------------------
    # 3. PID files
    # ------------------------------------------------------------
    pid_files = _find_matches(project_root, PID_PATTERNS)

    if pid_files:
        results.append(
            CheckResult(
                id="temp.pid",
                name="PID files detected",
                description="Stale PID files found.",
                status="warn",
                severity="medium",
                details="\n".join(str(p.relative_to(project_root)) for p in pid_files),
                plugin="temp_files",
            )
        )
    else:
        results.append(
            CheckResult(
                id="temp.pid.none",
                name="No PID files",
                description="No stale PID files detected.",
                status="ok",
                severity="info",
                plugin="temp_files",
            )
        )

    # ------------------------------------------------------------
    # 4. Large temp files
    # ------------------------------------------------------------
    large = _large_temp_files(temp_files)

    if large:
        results.append(
            CheckResult(
                id="temp.large",
                name="Large temporary files",
                description="Some temporary files are unusually large.",
                status="warn",
                severity="high",
                details="\n".join(large),
                plugin="temp_files",
            )
        )
    else:
        results.append(
            CheckResult(
                id="temp.large.none",
                name="No large temp files",
                description="No unusually large temporary files detected.",
                status="ok",
                severity="info",
                plugin="temp_files",
            )
        )

    return results
