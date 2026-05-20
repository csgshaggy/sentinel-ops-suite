"""
Doctor module

Provides:
- run_doctor(): main entrypoint for doctor checks
- Individual check functions (optional future expansion)

This file intentionally keeps the public API clean and stable.
"""

from .run_doctor import run_doctor

__all__ = [
    "run_doctor",
]
