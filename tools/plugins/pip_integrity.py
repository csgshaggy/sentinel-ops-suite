"""
SuperDoctor Plugin: Project Structure Validator
Location: tools/plugins/structure_validator.py

Checks:
- Required directories exist (tools/, tools/plugins/, tools/utils/, reports/)
- Required core files exist (super_doctor.py, html_reporter.py, history.py, scoring.py, modes.py, paths.py)
- Detects missing or misplaced modules
- Detects unexpected top-level files
- Validates plugin directory structure
"""

from pathlib import Path
from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Expected structure for ssrf-command-console
# ------------------------------------------------------------

REQUIRED_DIRS = [
    "tools",
    "tools/plugins",
    "tools/utils",
    "tools/reporting",
    "reports",
]

REQUIRED_FILES = [
    "tools/super_doctor.py",
    "tools/reporting/html_reporter.py",
    "tools/reporting/history.py",
    "tools/utils/paths.py",
    "tools/utils/scoring.py",
    "tools/utils/modes.py",
]


def _exists(project_root: Path, rel_path: str) -> bool:
    return (project_root / rel_path).exists()


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. Required directories
    # ------------------------------------------------------------
    missing_dirs = [d for d in REQUIRED_DIRS if not _exists(project_root, d)]

    if missing_dirs:
        results.append(
            CheckResult(
                id="structure.missing_dirs",
                name="Missing required directories",
                description="Some required directories are missing.",
                status="fail",
                severity="high",
                details="\n".join(missing_dirs),
                plugin="structure_validator",
            )
        )
    else:
        results.append(
            CheckResult(
                id="structure.dirs_ok",
                name="All required directories present",
                description="All required directories exist.",
                status="ok",
                severity="info",
                plugin="structure_validator",
            )
        )

    # ------------------------------------------------------------
    # 2. Required files
    # ------------------------------------------------------------
    missing_files = [f for f in REQUIRED_FILES if not _exists(project_root, f)]

    if missing_files:
        results.append(
            CheckResult(
                id="structure.missing_files",
                name="Missing required files",
                description="Some required core files are missing.",
                status="fail",
                severity="critical",
                details="\n".join(missing_files),
                plugin="structure_validator",
            )
        )
    else:
        results.append(
            CheckResult(
                id="structure.files_ok",
                name="All required files present",
                description="All required core files exist.",
                status="ok",
                severity="info",
                plugin="structure_validator",
            )
        )

    # ------------------------------------------------------------
    # 3. Plugin directory sanity
    # ------------------------------------------------------------
    plugins_dir = project_root / "tools" / "plugins"

    if not plugins_dir.exists():
        results.append(
            CheckResult(
                id="structure.plugins_missing",
                name="Plugins directory missing",
                description="tools/plugins directory does not exist.",
                status="fail",
                severity="high",
                plugin="structure_validator",
            )
        )
        return results

    plugin_files = [
        p.name for p in plugins_dir.glob("*.py") if not p.name.startswith("_")
    ]

    if not plugin_files:
        results.append(
            CheckResult(
                id="structure.no_plugins",
                name="No plugins found",
                description="tools/plugins contains no plugin files.",
                status="warn",
                severity="medium",
                plugin="structure_validator",
            )
        )
    else:
        results.append(
            CheckResult(
                id="structure.plugins_ok",
                name="Plugins detected",
                description=f"Found {len(plugin_files)} plugin(s).",
                status="ok",
                severity="info",
                details="\n".join(plugin_files),
                plugin="structure_validator",
            )
        )

    # ------------------------------------------------------------
    # 4. Unexpected top-level files
    # ------------------------------------------------------------
    allowed_top = {
        "tools",
        "reports",
        "requirements.txt",
        ".git",
        ".gitignore",
        "README.md",
    }

    unexpected = []
    for item in project_root.iterdir():
        if item.name not in allowed_top:
            unexpected.append(item.name)

    if unexpected:
        results.append(
            CheckResult(
                id="structure.unexpected_files",
                name="Unexpected top-level files",
                description="Found unexpected files or directories at project root.",
                status="warn",
                severity="low",
                details="\n".join(unexpected),
                plugin="structure_validator",
            )
        )
    else:
        results.append(
            CheckResult(
                id="structure.top_ok",
                name="Top-level structure clean",
                description="No unexpected files at project root.",
                status="ok",
                severity="info",
                plugin="structure_validator",
            )
        )

    return results
