"""
Execution modes for the SSRF Command Console.

These modes are used by:
- CLI tools
- Plugins
- Backend admin routes
- Structure validators
- The SuperDoctor system

They provide a consistent way to express how deeply or aggressively
a scan, validation, or health check should run.
"""

from __future__ import annotations

from enum import Enum


class Mode(str, Enum):
    """
    Execution mode for scanners, validators, and plugins.

    LOCAL  – Fast, minimal, safe checks. No external calls.
    FAST   – Medium-depth checks, optimized for speed.
    FULL   – Deep, exhaustive, forensic-grade analysis.
    """

    LOCAL = "local"
    FAST = "fast"
    FULL = "full"

    @classmethod
    def list(cls) -> list[str]:
        """Return all valid mode names."""
        return [m.value for m in cls]

    @classmethod
    def from_str(cls, value: str) -> "Mode":
        """
        Convert a string to a Mode enum, raising a clean error if invalid.
        """
        try:
            return cls(value.lower())
        except Exception:
            valid = ", ".join(cls.list())
            raise ValueError(f"Invalid mode '{value}'. Valid modes: {valid}")

    def is_local(self) -> bool:
        return self is Mode.LOCAL

    def is_fast(self) -> bool:
        return self is Mode.FAST

    def is_full(self) -> bool:
        return self is Mode.FULL
