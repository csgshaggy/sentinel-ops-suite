from __future__ import annotations

import subprocess
from typing import Any, Dict, List, Optional

PLUGIN_INFO = {
    "name": "git_status",
    "category": "scm",
    "entrypoint": "get_git_status",
}


def _run_git_command(args: List[str]) -> Optional[str]:
    """
    Run a Git command safely and return stdout or None on failure.
    """
    try:
        result = subprocess.run(
            ["git"] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=2,
        )
    except Exception:
        return None

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def get_git_status() -> Dict[str, Any]:
    """
    Return branch, commit, and working tree status.
    """
    branch = _run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    commit = _run_git_command(["rev-parse", "HEAD"])
    status_raw = _run_git_command(["status", "--porcelain"])

    if branch is None or commit is None:
        return {
            "success": False,
            "error": "Not a Git repository or Git is unavailable",
        }

    changes: List[str] = status_raw.splitlines() if status_raw else []

    return {
        "success": True,
        "branch": branch,
        "commit": commit,
        "changes": changes,
        "dirty": len(changes) > 0,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(get_git_status(), indent=2))
