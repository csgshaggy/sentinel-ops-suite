"""
SuperDoctor Plugin: Package Integrity & Import Health
Location: tools/plugins/package_integrity.py

Checks:
- Installed package metadata availability
- Missing or broken distributions
- Import failures
- Version mismatches (metadata vs import)
- Namespace collisions
- Duplicate distributions
- Cross-platform safe
"""

import importlib
import pkgutil
from pathlib import Path
from typing import List, Dict, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _safe_import(name: str) -> Optional[object]:
    """
    Attempt to import a module safely.
    Returns module or None.
    """
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def _get_distribution_version(name: str) -> Optional[str]:
    """
    Retrieve version from importlib.metadata.
    """
    try:
        from importlib.metadata import version

        return version(name)
    except Exception:
        return None


def _list_installed_packages() -> List[str]:
    """
    List top-level installed packages via pkgutil.
    """
    return sorted({m.name for m in pkgutil.iter_modules()})


def _detect_namespace_collisions(packages: List[str]) -> Dict[str, List[str]]:
    """
    Detect namespace collisions:
    - multiple packages providing the same top-level namespace
    """
    collisions: Dict[str, List[str]] = {}

    for pkg in packages:
        parts = pkg.split(".")
        if len(parts) > 1:
            top = parts[0]
            collisions.setdefault(top, []).append(pkg)

    # Only return namespaces with >1 provider
    return {k: v for k, v in collisions.items() if len(v) > 1}


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    packages = _list_installed_packages()

    # ------------------------------------------------------------
    # 1. Package import health
    # ------------------------------------------------------------
    import_failures = []

    for pkg in packages:
        mod = _safe_import(pkg)
        if mod is None:
            import_failures.append(pkg)

    if import_failures:
        results.append(
            CheckResult(
                id="pkg.import.failures",
                name="Import failures",
                description="Some installed packages could not be imported.",
                status="fail",
                severity="high",
                details="\n".join(import_failures),
                plugin="package_integrity",
            )
        )
    else:
        results.append(
            CheckResult(
                id="pkg.import.ok",
                name="All packages importable",
                description="No import failures detected.",
                status="ok",
                severity="info",
                plugin="package_integrity",
            )
        )

    # ------------------------------------------------------------
    # 2. Version mismatches
    # ------------------------------------------------------------
    mismatches = []

    for pkg in packages:
        meta_ver = _get_distribution_version(pkg)
        mod = _safe_import(pkg)

        if mod is None or meta_ver is None:
            continue

        # Try to get __version__ from module
        mod_ver = getattr(mod, "__version__", None)

        if mod_ver and mod_ver != meta_ver:
            mismatches.append(f"{pkg}: metadata={meta_ver}, module={mod_ver}")

    if mismatches:
        results.append(
            CheckResult(
                id="pkg.version.mismatch",
                name="Version mismatches",
                description="Metadata version differs from module __version__.",
                status="warn",
                severity="medium",
                details="\n".join(mismatches),
                plugin="package_integrity",
            )
        )
    else:
        results.append(
            CheckResult(
                id="pkg.version.ok",
                name="Version metadata consistent",
                description="No version mismatches detected.",
                status="ok",
                severity="info",
                plugin="package_integrity",
            )
        )

    # ------------------------------------------------------------
    # 3. Namespace collisions
    # ------------------------------------------------------------
    collisions = _detect_namespace_collisions(packages)

    if collisions:
        details = "\n".join(
            f"{ns}: {', '.join(pkgs)}" for ns, pkgs in collisions.items()
        )
        results.append(
            CheckResult(
                id="pkg.namespace.collisions",
                name="Namespace collisions",
                description="Multiple packages provide the same namespace.",
                status="warn",
                severity="high",
                details=details,
                plugin="package_integrity",
            )
        )
    else:
        results.append(
            CheckResult(
                id="pkg.namespace.ok",
                name="No namespace collisions",
                description="No namespace collisions detected.",
                status="ok",
                severity="info",
                plugin="package_integrity",
            )
        )

    # ------------------------------------------------------------
    # 4. Duplicate distributions (same package installed twice)
    # ------------------------------------------------------------
    try:
        from importlib.metadata import distributions

        dist_names = {}
        duplicates = []

        for dist in distributions():
            name = dist.metadata["Name"].lower()
            dist_names.setdefault(name, []).append(dist)

        for name, dists in dist_names.items():
            if len(dists) > 1:
                duplicates.append(name)

        if duplicates:
            results.append(
                CheckResult(
                    id="pkg.duplicates",
                    name="Duplicate distributions",
                    description="Some packages appear to be installed multiple times.",
                    status="warn",
                    severity="medium",
                    details="\n".join(duplicates),
                    plugin="package_integrity",
                )
            )
        else:
            results.append(
                CheckResult(
                    id="pkg.duplicates.none",
                    name="No duplicate distributions",
                    description="No duplicate package installs detected.",
                    status="ok",
                    severity="info",
                    plugin="package_integrity",
                )
            )
    except Exception:
        results.append(
            CheckResult(
                id="pkg.duplicates.unknown",
                name="Duplicate distribution check unavailable",
                description="Could not inspect installed distributions.",
                status="warn",
                severity="low",
                plugin="package_integrity",
            )
        )

    return results
