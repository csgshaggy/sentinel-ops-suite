"""
Base classes and protocols for drift detection plugins.
"""

from typing import Dict, Any, Protocol, runtime_checkable


@runtime_checkable
class DriftPlugin(Protocol):
    """
    A drift plugin must:
    - expose a `name` attribute
    - implement collect() -> dict
    """

    name: str

    def collect(self) -> Dict[str, Any]:
        ...
