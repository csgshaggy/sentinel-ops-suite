"""
IDRIM Exceptions
----------------
Canonical exception hierarchy for the IDRIM subsystem.

These exceptions are intentionally:
- Minimal
- Explicit
- Predictable
- Safe for API, CLI, and UI layers
"""

from __future__ import annotations


class IDRIMError(Exception):
    """Base class for all IDRIM-related errors."""
    pass


# ----------------------------------------------------------------------
# Request / Validation Errors
# ----------------------------------------------------------------------
class IDRIMInvalidRequestError(IDRIMError):
    """Raised when an IDRIMRequest is malformed or incomplete."""
    pass


# ----------------------------------------------------------------------
# Engine Errors
# ----------------------------------------------------------------------
class IDRIMEngineError(IDRIMError):
    """Raised when the IDRIMEngine encounters an unrecoverable failure."""
    pass


# ----------------------------------------------------------------------
# Task Runner Errors
# ----------------------------------------------------------------------
class IDRIMTaskError(IDRIMError):
    """Raised when async task execution fails."""
    pass
