"""
Git status plugin (sync).

Reports:
- current branch
- dirty state (modified, untracked, staged)
- ahead/behind counts
- last commit hash and timestamp

Forms the foundation for:
- CI drift detection
- repo hygiene enforcement
- operator console status indicators
"""

from __future__ import annotations

import subprocess
import time
from typing import Any, Dict

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports Git repository status.",
    "entrypoint": "run",
    "mode": "sync",
}


def _run(cmd: list[str]) -> str:
    """
    Safely run a git command and return stdout as text.
    """
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return ""


def _get_branch() -> str:
    return _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def _get_dirty() -> bool:
    return bool(_run(["git", "status", "--porcelain"]))  # any output = dirty


def _get_ahead_behind() -> Dict[str, int]:
    out = _run(["git", "rev-list", "--left-right", "--count", "HEAD...@{upstream}"])
    if not out:
        return {"ahead": 0, "behind": 0}

    try:
        ahead, behind = out.split()
        return {"ahead": int(ahead), "behind": int(behind)}
    except Exception:
        return {"ahead": 0, "behind": 0}


def _get_last_commit() -> Dict[str, Any]:
    commit_hash = _run(["git", "rev-parse", "HEAD"])
    commit_ts = _run(["git", "show", "-s", "--format=%ct", "HEAD"])
    try:
        commit_ts = int(commit_ts)
    except Exception:
        commit_ts = None

    return {
        "hash": commit_hash,
        "timestamp": commit_ts,
    }


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous Git status check.
    """
    try:
        branch = _get_branch()
        dirty = _get_dirty()
        ahead_behind = _get_ahead_behind()
        last_commit = _get_last_commit()

        if not branch:
            status = Status.WARN
            message = "Not a Git repository or unable to read Git status."
        elif dirty:
            status = Status.WARN
            message = "Repository has uncommitted changes."
        else:
            status = Status.OK
            message = "Git repository is clean."

        data = {
            "branch": branch,
            "dirty": dirty,
            "ahead": ahead_behind["ahead"],
            "behind": ahead_behind["behind"],
            "last_commit": last_commit,
            "mode": mode.value,
            "timestamp": time.time(),
        }

        return CheckResult(
            name=PLUGIN_INFO["name"],
            status=status,
            message=message,
            data=data,
        )

    except Exception as exc:
        return CheckResult.fail(
            name=PLUGIN_INFO["name"],
            message=f"Git status plugin failed: {exc}",
        )
