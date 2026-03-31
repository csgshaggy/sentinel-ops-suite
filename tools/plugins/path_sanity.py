"""
SuperDoctor Plugin: Path Sanity, Traversal Safety & Symlink Boundaries
Location: tools/plugins/path_sanity.py

Checks:
- Path normalization sanity
- Symlink escape detection
- Directory traversal hazards
- Project-root trust boundary enforcement
- Nonexistent or broken paths
- Cross-platform safe
"""

from pathlib import Path
from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _normalize(path: Path) -> Path:
    """
    Normalize a path safely.
    """
    try:
        return path.resolve()
    except Exception:
        return path.absolute()


def _symlink_escape(path: Path, root: Path) -> bool:
    """
    Detect if a symlink resolves outside the project root.
    """
    try:
        resolved = path.resolve()
        return root not in resolved.parents and resolved != root
    except Exception:
        return False


def _traversal_hazard(path: Path) -> bool:
    """
    Detect traversal patterns like ../ or absolute jumps.
    """
    s = str(path)
    return ".." in s or s.startswith("/") or s.startswith("\\") or ":" in s


def _broken_symlinks(root: Path) -> List[str]:
    broken = []
    for p in root.rglob("*"):
        try:
            if p.is_symlink() and not p.exists():
                broken.append(str(p.relative_to(root)))
        except Exception:
            continue
    return broken


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. Normalize project root
    # ------------------------------------------------------------
    normalized = _normalize(project_root)

    if normalized != project_root:
        results.append(
            CheckResult(
                id="path.normalized",
                name="Path normalization drift",
                description="Project root normalized path differs from raw path.",
                status="warn",
                severity="low",
                details=f"raw={project_root}\nnormalized={normalized}",
                plugin="path_sanity",
            )
        )
    else:
        results.append(
            CheckResult(
                id="path.normalized.ok",
                name="Path normalization OK",
                description="Project root path is stable and normalized.",
                status="ok",
                severity="info",
                plugin="path_sanity",
            )
        )

    # ------------------------------------------------------------
    # 2. Symlink escape detection
    # ------------------------------------------------------------
    escapes = []
    for p in project_root.rglob("*"):
        try:
            if p.is_symlink() and _symlink_escape(p, project_root):
                escapes.append(str(p.relative_to(project_root)))
        except Exception:
            continue

    if escapes:
        results.append(
            CheckResult(
                id="path.symlink.escape",
                name="Symlink trust-boundary escape",
                description="Some symlinks resolve outside the project root.",
                status="warn",
                severity="high",
                details="\n".join(escapes),
                plugin="path_sanity",
            )
        )
    else:
        results.append(
            CheckResult(
                id="path.symlink.ok",
                name="Symlinks safe",
                description="No symlink trust-boundary escapes detected.",
                status="ok",
                severity="info",
                plugin="path_sanity",
            )
        )

    # ------------------------------------------------------------
    # 3. Traversal hazards
    # ------------------------------------------------------------
    hazards = []
    for p in project_root.rglob("*"):
        if _traversal_hazard(p.relative_to(project_root)):
            hazards.append(str(p.relative_to(project_root)))

    if hazards:
        results.append(
            CheckResult(
                id="path.traversal",
                name="Traversal hazards",
                description="Paths contain traversal or absolute-jump patterns.",
                status="warn",
                severity="medium",
                details="\n".join(hazards),
                plugin="path_sanity",
            )
        )
    else:
        results.append(
            CheckResult(
                id="path.traversal.none",
                name="No traversal hazards",
                description="No directory traversal patterns detected.",
                status="ok",
                severity="info",
                plugin="path_sanity",
            )
        )

    # ------------------------------------------------------------
    # 4. Broken symlinks
    # ------------------------------------------------------------
    broken = _broken_symlinks(project_root)

    if broken:
        results.append(
            CheckResult(
                id="path.symlink.broken",
                name="Broken symlinks",
                description="Some symlinks point to nonexistent targets.",
                status="warn",
                severity="medium",
                details="\n".join(broken),
                plugin="path_sanity",
            )
        )
    else:
        results.append(
            CheckResult(
                id="path.symlink.broken.none",
                name="No broken symlinks",
                description="All symlinks resolve correctly.",
                status="ok",
                severity="info",
                plugin="path_sanity",
            )
        )

    return results
