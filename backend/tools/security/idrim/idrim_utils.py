"""
IDRIM Utilities
---------------
Small, deterministic helper functions used across the IDRIM subsystem.

This module intentionally avoids:
- State
- Side effects
- Heavy abstractions

Everything here must be safe to call from engine, service, tasks, or CLI.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional


# ----------------------------------------------------------------------
# Path Utilities
# ----------------------------------------------------------------------
def safe_resolve(path_str: str) -> Path:
    """
    Resolve a filesystem path safely and deterministically.

    Expands ~, resolves symlinks, and normalizes the path.
    """
    return Path(path_str).expanduser().resolve()


def hash_file(path: Path, chunk_size: int = 65536) -> Optional[str]:
    """
    Compute a SHA‑256 hash of a file.

    Returns None if the path is not a file.
    """
    if not path.is_file():
        return None

    sha = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha.update(chunk)

    return sha.hexdigest()


# ----------------------------------------------------------------------
# Simple Scoring Helpers
# ----------------------------------------------------------------------
def clamp_score(value: int, minimum: int = 0, maximum: int = 100) -> int:
    """
    Clamp a score to the 0‑100 range.
    """
    return max(minimum, min(maximum, value))
