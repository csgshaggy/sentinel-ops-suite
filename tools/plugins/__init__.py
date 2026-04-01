# Plugin registry for SSRF Command Console
# This file avoids importing heavy or optional plugins at module load time.

from .pelm import PELMPlugin

__all__ = [
    "PELMPlugin",
]

# Optional plugins can be imported lazily inside their callers.
