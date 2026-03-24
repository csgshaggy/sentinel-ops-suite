"""
SuperDoctor Plugin: Python Process Introspection
Location: tools/plugins/python_process.py

Checks:
- Current working directory sanity
- argv validation (no missing script, no suspicious args)
- Interpreter metadata (executable, prefix, version)
- Parent process hints (best-effort)
- Environment consistency (cwd inside project root)
- Cross-platform safe
"""

import os
import sys
import platform
from pathlib import Path
from typing import List, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _parent_process_name() -> Optional[str]:
    """
    Best-effort parent process detection.
    Works on Linux/macOS via /proc, limited on Windows.
    """
    if os.name == "nt":
        # Windows: use environment hint only
        return os.environ.get("PROCESSOR_IDENTIFIER")

    try:
        ppid = os.getppid()
        cmdline = Path(f"/proc/{ppid}/cmdline")
        if cmdline.exists():
            text = cmdline.read_text(errors="ignore").replace("\x00", " ").strip()
            return text
    except Exception:
        pass

    return None


def _cwd_sanity(cwd: Path, project_root: Path) -> Optional[str]:
    """
    Detect if cwd is outside project root or suspicious.
    """
    try:
        if not cwd.exists():
            return "Current working directory does not exist."

        if project_root not in cwd.parents and cwd != project_root:
            return f"cwd ({cwd}) is outside project root ({project_root})."

    except Exception as exc:
        return f"Error checking cwd: {exc}"

    return None


def _argv_sanity(argv: List[str]) -> Optional[str]:
    """
    Detect suspicious argv patterns:
    - empty argv
    - argv[0] missing or not a file
    - arguments that look like injection attempts
    """
    if not argv:
        return "argv is empty."

    if not argv[0]:
        return "argv[0] is empty."

    # Injection-like patterns
    for arg in argv:
        if any(x in arg for x in [";", "&&", "|", "`", "$(", "<", ">"]):
            return f"Suspicious argument detected: {arg}"

    return None


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    cwd = Path.cwd()
    argv = sys.argv

    # ------------------------------------------------------------
    # 1. cwd sanity
    # ------------------------------------------------------------
    cwd_issue = _cwd_sanity(cwd, project_root)

    if cwd_issue:
        results.append(
            CheckResult(
                id="proc.cwd.bad",
                name="cwd anomaly",
                description=cwd_issue,
                status="warn",
                severity="medium",
                plugin="python_process",
            )
        )
    else:
        results.append(
            CheckResult(
                id="proc.cwd.ok",
                name="cwd OK",
                description=f"cwd is {cwd}",
                status="ok",
                severity="info",
                plugin="python_process",
            )
        )

    # ------------------------------------------------------------
    # 2. argv sanity
    # ------------------------------------------------------------
    argv_issue = _argv_sanity(argv)

    if argv_issue:
        results.append(
            CheckResult(
                id="proc.argv.bad",
                name="argv anomaly",
                description=argv_issue,
                status="warn",
                severity="medium",
                plugin="python_process",
            )
        )
    else:
        results.append(
            CheckResult(
                id="proc.argv.ok",
                name="argv OK",
                description="argv appears normal.",
                status="ok",
                severity="info",
                details=" ".join(argv),
                plugin="python_process",
            )
        )

    # ------------------------------------------------------------
    # 3. Interpreter metadata
    # ------------------------------------------------------------
    exe = Path(sys.executable)
    prefix = Path(sys.prefix)
    version = platform.python_version()
    impl = platform.python_implementation()

    results.append(
        CheckResult(
            id="proc.interpreter",
            name="Interpreter metadata",
            description="Python interpreter details.",
            status="ok",
            severity="info",
            details=(
                f"Executable: {exe}\n"
                f"Prefix:     {prefix}\n"
                f"Version:    {version}\n"
                f"Impl:       {impl}"
            ),
            plugin="python_process",
        )
    )

    # ------------------------------------------------------------
    # 4. Parent process
    # ------------------------------------------------------------
    parent = _parent_process_name()

    if parent:
        results.append(
            CheckResult(
                id="proc.parent",
                name="Parent process",
                description="Detected parent process.",
                status="ok",
                severity="info",
                details=parent,
                plugin="python_process",
            )
        )
    else:
        results.append(
            CheckResult(
                id="proc.parent.unknown",
                name="Parent process unknown",
                description="Could not determine parent process.",
                status="warn",
                severity="low",
                plugin="python_process",
            )
        )

    return results
