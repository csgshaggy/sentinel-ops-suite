"""
GitMetadataPlugin

Captures:
- current branch
- latest commit hash
- working tree dirty/clean status
"""

import subprocess
from pathlib import Path
from typing import Dict, Any

from .base import DriftPlugin


class GitMetadataPlugin:
    name = "git_metadata"

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[2]

    def _run(self, *cmd: str) -> str:
        try:
            out = subprocess.check_output(
                cmd,
                cwd=self.root,
                stderr=subprocess.DEVNULL,
            )
            return out.decode().strip()
        except Exception:
            return "unknown"

    def collect(self) -> Dict[str, Any]:
        return {
            "branch": self._run("git", "rev-parse", "--abbrev-ref", "HEAD"),
            "commit": self._run("git", "rev-parse", "HEAD"),
            "status": self._run("git", "status", "--porcelain"),
        }
