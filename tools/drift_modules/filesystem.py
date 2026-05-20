"""
FilesystemHashPlugin

Produces deterministic SHA256 hashes of all files in the repo,
excluding .git, .drift, and __pycache__.
"""

import hashlib
import os
from pathlib import Path
from typing import Dict, Any

from .base import DriftPlugin


class FilesystemHashPlugin:
    name = "filesystem_hash"

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[2]

    def _iter_files(self):
        ignore_dirs = {".git", ".drift", "__pycache__"}
        files = []

        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

            for fname in filenames:
                full = Path(dirpath) / fname
                try:
                    full.relative_to(self.root)
                except ValueError:
                    continue
                files.append(full)

        return sorted(files, key=lambda p: str(p.relative_to(self.root)))

    def _hash_file(self, path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def collect(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for f in self._iter_files():
            rel = str(f.relative_to(self.root))
            result[rel] = self._hash_file(f)
        return result
