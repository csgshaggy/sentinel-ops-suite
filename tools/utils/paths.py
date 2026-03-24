"""
Cross‑platform path utilities for SuperDoctor
Location: tools/utils/paths.py

Provides:
- get_project_root()      → resolves ssrf-command-console root
- ensure_directory(path)  → mkdir -p (Windows + Linux safe)
- to_relative_path(path)  → clean relative paths for reports/logs
"""

from pathlib import Path
from typing import Optional


# ------------------------------------------------------------
# Project root detection
# ------------------------------------------------------------


def get_project_root() -> Path:
    """
    Resolve the project root directory (ssrf-command-console).

    This works even when:
    - running from venv/bin/python
    - running from Windows PowerShell
    - running from CI
    - running from a packaged EXE (PyInstaller/Nuitka)

    Strategy:
    - Start from this file's location
    - Walk upward until we find the project root folder name
    """
    current = Path(__file__).resolve()

    # Walk upward until we find the project root
    for parent in current.parents:
        if parent.name == "ssrf-command-console":
            return parent

    # Fallback: assume current working directory is project root
    return Path.cwd()


# ------------------------------------------------------------
# Directory creation
# ------------------------------------------------------------


def ensure_directory(path: Path) -> None:
    """
    Create a directory if it doesn't exist.
    Cross‑platform safe (Windows + Linux).
    """
    path.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Relative path helper
# ------------------------------------------------------------


def to_relative_path(path: Path, base: Optional[Path] = None) -> str:
    """
    Convert an absolute path to a clean relative path for display.
    If base is not provided, use project root.
    """
    if base is None:
        base = get_project_root()

    try:
        return str(path.relative_to(base))
    except Exception:
        return str(path)
