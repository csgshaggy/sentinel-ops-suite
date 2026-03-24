"""
SuperDoctor Plugin: Python Environment Validation
Location: tools/plugins/python_env.py

Checks:
- Python version meets minimum requirement
- Python implementation (CPython vs PyPy)
- sys.path sanity
- Required core modules import cleanly
- Interpreter consistency (prefix, executable)
"""

import sys
import platform
from pathlib import Path
from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode


MIN_PYTHON = (3, 10)  # Minimum supported version


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. Python version
    # ------------------------------------------------------------
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if (version.major, version.minor) < MIN_PYTHON:
        results.append(
            CheckResult(
                id="python.version.too_low",
                name="Python version too low",
                description=f"Python {version_str} is below the minimum required {MIN_PYTHON[0]}.{MIN_PYTHON[1]}.",
                status="fail",
                severity="high",
                plugin="python_env",
            )
        )
    else:
        results.append(
            CheckResult(
                id="python.version.ok",
                name="Python version OK",
                description=f"Python {version_str} meets minimum requirements.",
                status="ok",
                severity="info",
                plugin="python_env",
            )
        )

    # ------------------------------------------------------------
    # 2. Python implementation
    # ------------------------------------------------------------
    impl = platform.python_implementation()

    if impl != "CPython":
        results.append(
            CheckResult(
                id="python.impl.non_cpython",
                name="Non-CPython interpreter",
                description=f"Running on {impl}. Some tooling may not behave consistently.",
                status="warn",
                severity="medium",
                plugin="python_env",
            )
        )
    else:
        results.append(
            CheckResult(
                id="python.impl.cpython",
                name="CPython interpreter",
                description="Running on CPython.",
                status="ok",
                severity="info",
                plugin="python_env",
            )
        )

    # ------------------------------------------------------------
    # 3. sys.path sanity check
    # ------------------------------------------------------------
    bad_paths = [p for p in sys.path if p and not Path(p).exists()]

    if bad_paths:
        results.append(
            CheckResult(
                id="python.syspath.bad_entries",
                name="Invalid sys.path entries",
                description="Some sys.path entries do not exist.",
                status="warn",
                severity="low",
                details="\n".join(bad_paths),
                plugin="python_env",
            )
        )
    else:
        results.append(
            CheckResult(
                id="python.syspath.ok",
                name="sys.path valid",
                description="All sys.path entries exist.",
                status="ok",
                severity="info",
                plugin="python_env",
            )
        )

    # ------------------------------------------------------------
    # 4. Core module imports
    # ------------------------------------------------------------
    core_modules = ["json", "pathlib", "subprocess", "importlib"]

    for mod in core_modules:
        try:
            __import__(mod)
            results.append(
                CheckResult(
                    id=f"python.module.{mod}.ok",
                    name=f"Module import OK: {mod}",
                    description=f"Successfully imported {mod}.",
                    status="ok",
                    severity="info",
                    plugin="python_env",
                )
            )
        except Exception as exc:
            results.append(
                CheckResult(
                    id=f"python.module.{mod}.fail",
                    name=f"Module import failed: {mod}",
                    description=f"Failed to import {mod}.",
                    status="fail",
                    severity="high",
                    details=str(exc),
                    plugin="python_env",
                )
            )

    # ------------------------------------------------------------
    # 5. Interpreter consistency
    # ------------------------------------------------------------
    exe = Path(sys.executable)
    prefix = Path(sys.prefix)

    if prefix not in exe.parents:
        results.append(
            CheckResult(
                id="python.interpreter.mismatch",
                name="Interpreter prefix mismatch",
                description="Python executable is not located inside sys.prefix.",
                status="warn",
                severity="medium",
                details=f"Executable: {exe}\nPrefix: {prefix}",
                plugin="python_env",
            )
        )
    else:
        results.append(
            CheckResult(
                id="python.interpreter.ok",
                name="Interpreter prefix OK",
                description="Python executable matches sys.prefix.",
                status="ok",
                severity="info",
                plugin="python_env",
            )
        )

    return results
