"""
tools/super_doctor.py

Shared health-check primitives used by:
- plugins
- doctor
- structure validators
- scoring utilities
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict


class Status(str, Enum):
    OK = "ok"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class CheckResult:
    """
    Standardized result object for all health checks.

    Attributes:
        name: Name of the check or plugin.
        status: One of Status.OK, Status.WARN, Status.FAIL.
        message: Human-readable summary.
        data: Optional structured metadata for dashboards or logs.
    """

    name: str
    status: Status
    message: str
    data: Dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------

    @classmethod
    def ok(cls, name: str, message: str = "OK", data: Dict[str, Any] | None = None):
        return cls(name=name, status=Status.OK, message=message, data=data)

    @classmethod
    def warn(cls, name: str, message: str, data: Dict[str, Any] | None = None):
        return cls(name=name, status=Status.WARN, message=message, data=data)

    @classmethod
    def fail(cls, name: str, message: str, data: Dict[str, Any] | None = None):
        return cls(name=name, status=Status.FAIL, message=message, data=data)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-safe dictionary representation."""
        d = asdict(self)
        d["status"] = self.status.value
        return d

    def __str__(self) -> str:
        return f"[{self.status.upper()}] {self.name}: {self.message}"
