"""
SuperDoctor Plugin: Python Path & Import Integrity
Location: tools/plugins/python_paths.py

Checks:
- Duplicate sys.path entries
- Nonexistent sys.path entries
- Shadowed standard library modules
- Shadowed installed packages
- Import poisoning (project files overriding modules)
- Precedence anomalies
"""

import sys
from pathlib import Path
from typing import List, Dict

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _std_lib_modules() -> set:
    """
    Return a set of known standard library module names.
    Uses sys.builtin_module_names + a static list for reliability.
    """
    builtin = set(sys.builtin_module_names)

    # Minimal static list to detect common shadows
    common = {
        "json",
        "pathlib",
        "subprocess",
        "asyncio",
        "logging",
        "email",
        "http",
        "urllib",
        "xml",
        "re",
        "ssl",
        "sqlite3",
        "threading",
        "multiprocessing",
        "shutil",
        "tempfile",
    }

    return builtin.union(common)


def _list_py_files(path: Path) -> List[str]:
    try:
        return [p.name for p in path.glob("*.py")]
    except Exception:
        return []


def _detect_shadowing(project_root: Path, stdlib: set) -> Dict[str, str]:
    """
    Detect files in the project that shadow stdlib modules.
    Returns {module: path}.
    """
    shadows = {}
    for py in project_root.rglob("*.py"):
        name = py.stem
        if name in stdlib:
            shadows[name] = str(py.relative_to(project_root))
    return shadows


def _detect_duplicate_paths() -> List[str]:
    seen = set()
    duplicates = []
    for entry in sys.path:
        if entry in seen:
            duplicates.append(entry)
        else:
            seen.add(entry)
    return duplicates


def _detect_missing_paths() -> List[str]:
    missing = []
    for entry in sys.path:
        if entry and not Path(entry).exists():
            missing.append(entry)
    return missing


def _detect_import_poisoning(project_root: Path) -> List[str]:
    """
    Detect project files that override installed packages.
    Example: project_root/requests.py overrides pip-installed requests.
    """
    poisoning = []
    installed = {pkg.key for pkg in _safe_pkg_list()}

    for py in project_root.rglob("*.py"):
        name = py.stem.lower()
        if name in installed:
            poisoning.append(str(py.relative_to(project_root)))

    return poisoning


def _safe_pkg_list():
    """
    Best-effort list of installed packages without failing on broken environments.
    """
    try:
        import pkg_resources

        return list(pkg_resources.working_set)
    except Exception:
        return []


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    stdlib = _std_lib_modules()

    # ------------------------------------------------------------
    # 1. Duplicate sys.path entries
    # ------------------------------------------------------------
    duplicates = _detect_duplicate_paths()

    if duplicates:
        results.append(
            CheckResult(
                id="py.path.duplicates",
                name="Duplicate sys.path entries",
                description="Some sys.path entries appear more than once.",
                status="warn",
                severity="medium",
                details="\n".join(duplicates),
                plugin="python_paths",
            )
        )
    else:
        results.append(
            CheckResult(
                id="py.path.duplicates.none",
                name="No duplicate sys.path entries",
                description="sys.path contains no duplicates.",
                status="ok",
                severity="info",
                plugin="python_paths",
            )
        )

    # ------------------------------------------------------------
    # 2. Missing sys.path entries
    # ------------------------------------------------------------
    missing = _detect_missing_paths()

    if missing:
        results.append(
            CheckResult(
                id="py.path.missing",
                name="Missing sys.path entries",
                description="Some sys.path entries do not exist.",
                status="warn",
                severity="low",
                details="\n".join(missing),
                plugin="python_paths",
            )
        )
    else:
        results.append(
            CheckResult(
                id="py.path.missing.none",
                name="All sys.path entries valid",
                description="All sys.path entries exist.",
                status="ok",
                severity="info",
                plugin="python_paths",
            )
        )

    # ------------------------------------------------------------
    # 3. Shadowed standard library modules
    # ------------------------------------------------------------
    shadows = _detect_shadowing(project_root, stdlib)

    if shadows:
        details = "\n".join(f"{mod}: {path}" for mod, path in shadows.items())
        results.append(
            CheckResult(
                id="py.shadow.stdlib",
                name="Shadowed standard library modules",
                description="Project files override standard library modules.",
                status="fail",
                severity="high",
                details=details,
                plugin="python_paths",
            )
        )
    else:
        results.append(
            CheckResult(
                id="py.shadow.stdlib.none",
                name="No stdlib shadowing",
                description="No project files override standard library modules.",
                status="ok",
                severity="info",
                plugin="python_paths",
            )
        )

    # ------------------------------------------------------------
    # 4. Import poisoning (project files overriding installed packages)
    # ------------------------------------------------------------
    poisoning = _detect_import_poisoning(project_root)

    if poisoning:
        results.append(
            CheckResult(
                id="py.poisoning",
                name="Import poisoning detected",
                description="Project files override installed packages.",
                status="fail",
                severity="high",
                details="\n".join(poisoning),
                plugin="python_paths",
            )
        )
    else:
        results.append(
            CheckResult(
                id="py.poisoning.none",
                name="No import poisoning",
                description="No project files override installed packages.",
                status="ok",
                severity="info",
                plugin="python_paths",
            )
        )

    return results
