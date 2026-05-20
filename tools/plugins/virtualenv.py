"""
SuperDoctor Plugin: Virtual Environment Integrity
Location: tools/plugins/virtualenv.py

Checks:
- VIRTUAL_ENV environment variable presence
- Interpreter prefix vs VIRTUAL_ENV consistency
- sys.base_prefix vs sys.prefix drift
- pip executable location sanity
- Package install location sanity
- Cross-platform safe
"""

import os
import sys
from pathlib import Path
from typing import List, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _pip_location() -> Optional[Path]:
    """
    Locate pip inside the active environment.
    """
    prefix = Path(sys.prefix)

    # POSIX
    candidate = prefix / "bin" / "pip"
    if candidate.exists():
        return candidate

    # Windows
    candidate = prefix / "Scripts" / "pip.exe"
    if candidate.exists():
        return candidate

    return None


def _is_inside_venv() -> bool:
    """
    Detect if Python is running inside a virtual environment.
    """
    return sys.prefix != sys.base_prefix


def _venv_root_from_prefix() -> Path:
    """
    Infer venv root from sys.prefix.
    """
    return Path(sys.prefix)


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    env_var = os.environ.get("VIRTUAL_ENV")
    inside_venv = _is_inside_venv()
    prefix = Path(sys.prefix)
    base_prefix = Path(sys.base_prefix)

    # ------------------------------------------------------------
    # 1. VIRTUAL_ENV environment variable
    # ------------------------------------------------------------
    if env_var:
        results.append(
            CheckResult(
                id="venv.envvar.present",
                name="VIRTUAL_ENV present",
                description=f"VIRTUAL_ENV is set to {env_var}.",
                status="ok",
                severity="info",
                plugin="virtualenv",
            )
        )
    else:
        results.append(
            CheckResult(
                id="venv.envvar.missing",
                name="VIRTUAL_ENV missing",
                description="VIRTUAL_ENV environment variable is not set.",
                status="warn",
                severity="medium",
                plugin="virtualenv",
            )
        )

    # ------------------------------------------------------------
    # 2. Interpreter inside venv?
    # ------------------------------------------------------------
    if inside_venv:
        results.append(
            CheckResult(
                id="venv.active",
                name="Virtual environment active",
                description="Python interpreter is running inside a virtual environment.",
                status="ok",
                severity="info",
                details=f"prefix={prefix}\nbase_prefix={base_prefix}",
                plugin="virtualenv",
            )
        )
    else:
        results.append(
            CheckResult(
                id="venv.inactive",
                name="Virtual environment NOT active",
                description="Python interpreter is NOT running inside a virtual environment.",
                status="warn",
                severity="high",
                plugin="virtualenv",
            )
        )

    # ------------------------------------------------------------
    # 3. VIRTUAL_ENV matches sys.prefix?
    # ------------------------------------------------------------
    if env_var:
        env_path = Path(env_var)
        if env_path.resolve() != prefix.resolve():
            results.append(
                CheckResult(
                    id="venv.mismatch",
                    name="VIRTUAL_ENV mismatch",
                    description="VIRTUAL_ENV does not match sys.prefix.",
                    status="warn",
                    severity="medium",
                    details=f"VIRTUAL_ENV={env_path}\nsys.prefix={prefix}",
                    plugin="virtualenv",
                )
            )
        else:
            results.append(
                CheckResult(
                    id="venv.match",
                    name="VIRTUAL_ENV matches sys.prefix",
                    description="Environment variable and interpreter prefix align.",
                    status="ok",
                    severity="info",
                    plugin="virtualenv",
                )
            )

    # ------------------------------------------------------------
    # 4. pip location sanity
    # ------------------------------------------------------------
    pip_path = _pip_location()

    if pip_path is None:
        results.append(
            CheckResult(
                id="venv.pip.missing",
                name="pip executable missing",
                description="pip executable not found inside the active environment.",
                status="warn",
                severity="high",
                plugin="virtualenv",
            )
        )
    else:
        results.append(
            CheckResult(
                id="venv.pip.ok",
                name="pip executable OK",
                description="pip executable found inside the active environment.",
                status="ok",
                severity="info",
                details=str(pip_path),
                plugin="virtualenv",
            )
        )

    # ------------------------------------------------------------
    # 5. Package install location sanity
    # ------------------------------------------------------------
    try:
        import site

        site_paths = site.getsitepackages()
        bad = [p for p in site_paths if not Path(p).exists()]
    except Exception:
        site_paths = []
        bad = []

    if bad:
        results.append(
            CheckResult(
                id="venv.site.bad",
                name="Invalid site-packages paths",
                description="Some site-packages paths do not exist.",
                status="warn",
                severity="medium",
                details="\n".join(bad),
                plugin="virtualenv",
            )
        )
    else:
        results.append(
            CheckResult(
                id="venv.site.ok",
                name="site-packages OK",
                description="All site-packages paths exist.",
                status="ok",
                severity="info",
                plugin="virtualenv",
            )
        )

    return results
