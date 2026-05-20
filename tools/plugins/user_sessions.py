"""
User sessions plugin (sync).

Reports:
- currently logged‑in users
- active TTY sessions
- remote SSH sessions
- session counts and anomalies

Forms the foundation for:
- detecting unexpected remote access
- correlating session activity with audit logs
- CI baseline enforcement for expected user presence
"""

from __future__ import annotations

import subprocess
import time
from typing import Any, Dict, List

from tools.super_doctor import CheckResult, Status
from utils.modes import Mode

PLUGIN_INFO: Dict[str, Any] = {
    "name": __name__.split(".")[-1],
    "description": "Reports active user login sessions.",
    "entrypoint": "run",
    "mode": "sync",
}


def _run_cmd(cmd: List[str]) -> str:
    """
    Safely run a command and return stdout as text.
    """
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except Exception:
        return ""


def _parse_who_output(output: str) -> List[Dict[str, Any]]:
    """
    Parse the output of the `who` command.
    """
    sessions = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue

        entry = {
            "user": parts[0],
            "tty": parts[1],
            "details": " ".join(parts[2:]) if len(parts) > 2 else "",
        }
        sessions.append(entry)

    return sessions


def run(mode: Mode = Mode.FAST) -> CheckResult:
    """
    Synchronous user session check.
    """
    try:
        raw = _run_cmd(["who"])
        sessions = _parse_who_output(raw)

        ssh_sessions = [
            s for s in sessions if "pts" in s["tty"] or "ssh" in s["details"].lower()
        ]

        if len(sessions) == 0:
            status = Status.OK
            message = "No active user sessions detected."
        elif len(ssh_sessions) > 0:
            status = Status.WARN
            message = f"Remote/SSH sessions detected: {len(ssh_sessions)}"
        else:
            status = Status.OK
            message = "Local user sessions active."

        data = {
            "sessions": sessions,
            "session_count": len(sessions),
            "ssh_session_count": len(ssh_sessions),
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
            message=f"User sessions plugin failed: {exc}",
        )
