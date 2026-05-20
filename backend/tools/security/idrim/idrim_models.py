"""
IDRIM Models
------------
Canonical request/response structures for the IDRIM subsystem.

These models are intentionally:
- Deterministic
- Validation‑friendly
- CI‑safe
- Free of business logic
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


# ----------------------------------------------------------------------
# Request Model
# ----------------------------------------------------------------------
@dataclass
class IDRIMRequest:
    """
    Input structure for IDRIM analysis.

    Fields:
    - target_path: Path to file or directory to inspect
    - options: Optional dict for future extensibility (flags, modes, etc.)
    """

    target_path: str
    options: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.target_path, str) or not self.target_path.strip():
            raise ValueError("IDRIMRequest.target_path must be a non‑empty string")


# ----------------------------------------------------------------------
# Result Model
# ----------------------------------------------------------------------
@dataclass
class IDRIMResult:
    """
    Output structure for IDRIM analysis.

    Fields:
    - target: Resolved target path
    - file_count: Number of files inspected
    - dir_count: Number of directories inspected
    - score: Deterministic score (0‑100)
    - metadata: Arbitrary engine metadata
    """

    target: str
    file_count: int
    dir_count: int
    score: int
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.score, int) or not (0 <= self.score <= 100):
            raise ValueError("IDRIMResult.score must be an integer between 0 and 100")
