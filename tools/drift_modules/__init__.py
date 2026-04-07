"""
Sentinel Ops Suite — Drift Modules Package
Central registry for all drift detection plugins.
Each plugin must expose:
    - name: str
    - collect(root: Path) -> dict
"""

from .filesystem_hash import FilesystemHashPlugin
from .git_metadata import GitMetadataPlugin

# Ordered plugin registry
PLUGINS = [
    FilesystemHashPlugin(),
    GitMetadataPlugin(),
]

__all__ = [
    "PLUGINS",
    "FilesystemHashPlugin",
    "GitMetadataPlugin",
]
