import os
from pathlib import Path


class GitMetadataPlugin:
    """
    Collects minimal, deterministic Git metadata for drift detection.
    """

    name = "git_metadata"

    def collect(self, root: Path) -> dict:
        branch = os.popen("git rev-parse --abbrev-ref HEAD 2>/dev/null").read().strip()
        commit = os.popen("git rev-parse HEAD 2>/dev/null").read().strip()
        status = os.popen("git status --porcelain 2>/dev/null").read().strip().splitlines()

        return {
            "branch": branch,
            "commit": commit,
            "working_tree_clean": len(status) == 0,
            "changes": status,
        }
