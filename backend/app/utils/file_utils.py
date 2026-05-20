# app/utils/file_utils.py

import difflib
import os
import shutil
from typing import Dict, List

# ------------------------------------------------------------
# Basic file helpers
# ------------------------------------------------------------


def read_file_lines(path: str) -> List[str]:
    """
    Read a file and return its lines.
    Raises FileNotFoundError if missing.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r") as f:
        return f.readlines()


def write_file(path: str, content: str) -> None:
    """
    Write text content to a file.
    Creates directories if needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


# ------------------------------------------------------------
# Makefile reference generator
# ------------------------------------------------------------


def ensure_reference_makefile() -> Dict[str, str]:
    """
    Copy backend/Makefile → backend/Makefile.reference.
    Used to reset the baseline for diffing.
    """
    src = "backend/Makefile"
    dst = "backend/Makefile.reference"

    if not os.path.exists(src):
        raise FileNotFoundError("backend/Makefile not found")

    shutil.copyfile(src, dst)

    return {"source": src, "reference": dst, "status": "reference updated"}


# ------------------------------------------------------------
# Diff helpers
# ------------------------------------------------------------


def unified_diff(current: List[str], reference: List[str]) -> List[str]:
    """
    Produce a unified diff between two lists of lines.
    """
    diff = difflib.unified_diff(
        current,
        reference,
        fromfile="Makefile (current)",
        tofile="Makefile (reference)",
        lineterm="",
    )
    return list(diff)


def compute_health_score(diff_lines: List[str]) -> int:
    """
    Compute a simple health score:
    - 100 = perfect match
    - lower score = more drift
    """
    if not diff_lines:
        return 100

    penalty = min(len(diff_lines) * 2, 80)
    return max(20, 100 - penalty)


# ------------------------------------------------------------
# Safe file existence checks
# ------------------------------------------------------------


def file_exists(path: str) -> bool:
    """Return True if a file exists."""
    return os.path.exists(path)


def ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)
