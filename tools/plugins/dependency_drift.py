"""
SuperDoctor Plugin: Dependency Drift Detection
Location: tools/plugins/dependency_drift.py

Checks:
- requirements.txt exists
- requirements.txt is parseable
- Installed packages match requirements
- Missing packages
- Extra packages
- Version mismatches
- Import availability for required modules
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _read_requirements(req_path: Path) -> Dict[str, str]:
    """
    Parse requirements.txt into {package: version or None}.
    Supports:
        pkg==1.2.3
        pkg>=1.0
        pkg
    """
    reqs = {}
    for line in req_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if "==" in line:
            pkg, ver = line.split("==", 1)
            reqs[pkg.lower()] = ver
        elif ">=" in line:
            pkg, ver = line.split(">=", 1)
            reqs[pkg.lower()] = f">={ver}"
        else:
            reqs[line.lower()] = None

    return reqs


def _pip_freeze() -> Dict[str, str]:
    """
    Returns installed packages as {package: version}.
    Cross‑platform safe.
    """
    try:
        out = subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return {}

    pkgs = {}
    for line in out.splitlines():
        if "==" in line:
            pkg, ver = line.split("==", 1)
            pkgs[pkg.lower()] = ver
    return pkgs


def _import_test(pkg: str) -> Tuple[bool, str]:
    """
    Try importing a package to verify runtime availability.
    """
    try:
        __import__(pkg)
        return True, ""
    except Exception as exc:
        return False, str(exc)


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    req_path = project_root / "requirements.txt"

    # ------------------------------------------------------------
    # 1. requirements.txt exists
    # ------------------------------------------------------------
    if not req_path.exists():
        results.append(
            CheckResult(
                id="deps.requirements_missing",
                name="requirements.txt missing",
                description="No requirements.txt found at project root.",
                status="warn",
                severity="medium",
                plugin="dependency_drift",
            )
        )
        return results

    results.append(
        CheckResult(
            id="deps.requirements_present",
            name="requirements.txt found",
            description="requirements.txt exists.",
            status="ok",
            severity="info",
            plugin="dependency_drift",
        )
    )

    # ------------------------------------------------------------
    # 2. Parse requirements.txt
    # ------------------------------------------------------------
    try:
        reqs = _read_requirements(req_path)
    except Exception as exc:
        results.append(
            CheckResult(
                id="deps.requirements_parse_error",
                name="Failed to parse requirements.txt",
                description="requirements.txt could not be parsed.",
                status="fail",
                severity="high",
                details=str(exc),
                plugin="dependency_drift",
            )
        )
        return results

    # ------------------------------------------------------------
    # 3. Get installed packages
    # ------------------------------------------------------------
    installed = _pip_freeze()

    # ------------------------------------------------------------
    # 4. Compare required vs installed
    # ------------------------------------------------------------
    missing = []
    extra = []
    mismatched = []

    for pkg, req_ver in reqs.items():
        if pkg not in installed:
            missing.append(pkg)
            continue

        if req_ver and "==" in req_ver:
            # Exact version required
            if installed[pkg] != req_ver:
                mismatched.append((pkg, req_ver, installed[pkg]))

    # Extra packages (installed but not required)
    for pkg in installed:
        if pkg not in reqs:
            extra.append(pkg)

    # ------------------------------------------------------------
    # 5. Report missing packages
    # ------------------------------------------------------------
    if missing:
        results.append(
            CheckResult(
                id="deps.missing",
                name="Missing required packages",
                description="Some required packages are not installed.",
                status="fail",
                severity="high",
                details="\n".join(missing),
                plugin="dependency_drift",
            )
        )
    else:
        results.append(
            CheckResult(
                id="deps.missing.none",
                name="No missing packages",
                description="All required packages are installed.",
                status="ok",
                severity="info",
                plugin="dependency_drift",
            )
        )

    # ------------------------------------------------------------
    # 6. Report version mismatches
    # ------------------------------------------------------------
    if mismatched:
        details = "\n".join(
            f"{pkg}: required {req}, installed {inst}" for pkg, req, inst in mismatched
        )
        results.append(
            CheckResult(
                id="deps.version_mismatch",
                name="Version mismatches",
                description="Some packages do not match required versions.",
                status="warn",
                severity="medium",
                details=details,
                plugin="dependency_drift",
            )
        )
    else:
        results.append(
            CheckResult(
                id="deps.version_mismatch.none",
                name="No version mismatches",
                description="Installed package versions match requirements.",
                status="ok",
                severity="info",
                plugin="dependency_drift",
            )
        )

    # ------------------------------------------------------------
    # 7. Report extra packages
    # ------------------------------------------------------------
    if extra:
        results.append(
            CheckResult(
                id="deps.extra",
                name="Extra packages installed",
                description="Packages installed but not listed in requirements.txt.",
                status="warn",
                severity="low",
                details="\n".join(extra),
                plugin="dependency_drift",
            )
        )
    else:
        results.append(
            CheckResult(
                id="deps.extra.none",
                name="No extra packages",
                description="No unexpected packages installed.",
                status="ok",
                severity="info",
                plugin="dependency_drift",
            )
        )

    # ------------------------------------------------------------
    # 8. Import tests for required packages
    # ------------------------------------------------------------
    for pkg in reqs:
        ok, err = _import_test(pkg)
        if ok:
            results.append(
                CheckResult(
                    id=f"deps.import.{pkg}.ok",
                    name=f"Import OK: {pkg}",
                    description=f"Successfully imported {pkg}.",
                    status="ok",
                    severity="info",
                    plugin="dependency_drift",
                )
            )
        else:
            results.append(
                CheckResult(
                    id=f"deps.import.{pkg}.fail",
                    name=f"Import failed: {pkg}",
                    description=f"Failed to import required package {pkg}.",
                    status="fail",
                    severity="high",
                    details=err,
                    plugin="dependency_drift",
                )
            )

    return results
