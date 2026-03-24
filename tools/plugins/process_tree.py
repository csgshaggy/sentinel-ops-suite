"""
SuperDoctor Plugin: Process Tree & Execution Chain Inspector
Location: tools/plugins/process_tree.py

Checks:
- Parent/child process mapping
- Orphaned processes (best-effort)
- Zombie processes (POSIX)
- Exec-chain anomalies
- Process command-line capture
- Cross-platform safe
"""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _ps_list() -> Optional[str]:
    """
    Cross-platform process listing.
    """
    try:
        if os.name == "nt":
            # Windows: use wmic or powershell
            cmd = ["wmic", "process", "get", "ProcessId,ParentProcessId,CommandLine"]
            return subprocess.check_output(cmd, text=True, errors="ignore")
        else:
            # POSIX: use ps
            cmd = ["ps", "-eo", "pid,ppid,state,command"]
            return subprocess.check_output(cmd, text=True, errors="ignore")
    except Exception:
        return None


def _parse_ps(output: str) -> List[Dict[str, str]]:
    """
    Parse ps output into structured rows.
    """
    rows = []
    for line in output.splitlines()[1:]:
        parts = line.strip().split(None, 3)
        if len(parts) < 3:
            continue

        if os.name == "nt":
            # WMIC output is messy; best-effort parsing
            # Expect: CommandLine, ParentProcessId, ProcessId
            try:
                cmd, ppid, pid = parts[-3:]
            except Exception:
                continue
            rows.append({"pid": pid, "ppid": ppid, "state": "?", "cmd": cmd})
        else:
            pid, ppid, state, cmd = (
                parts[0],
                parts[1],
                parts[2],
                parts[3] if len(parts) > 3 else "",
            )
            rows.append({"pid": pid, "ppid": ppid, "state": state, "cmd": cmd})

    return rows


def _detect_zombies(rows: List[Dict[str, str]]) -> List[str]:
    """
    POSIX zombie detection: state == 'Z'
    """
    if os.name == "nt":
        return []
    return [r["pid"] for r in rows if r["state"].startswith("Z")]


def _build_tree(rows: List[Dict[str, str]]) -> Dict[str, List[str]]:
    """
    Build parent -> children mapping.
    """
    tree = {}
    for r in rows:
        tree.setdefault(r["ppid"], []).append(r["pid"])
    return tree


def _orphans(rows: List[Dict[str, str]]) -> List[str]:
    """
    Processes whose parent does not exist in the table.
    """
    pids = {r["pid"] for r in rows}
    orphans = [r["pid"] for r in rows if r["ppid"] not in pids and r["ppid"] != "0"]
    return orphans


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    output = _ps_list()

    if not output:
        results.append(
            CheckResult(
                id="proc.tree.unavailable",
                name="Process listing unavailable",
                description="Could not retrieve process list.",
                status="warn",
                severity="medium",
                plugin="process_tree",
            )
        )
        return results

    rows = _parse_ps(output)

    # ------------------------------------------------------------
    # 1. Zombie processes
    # ------------------------------------------------------------
    zombies = _detect_zombies(rows)

    if zombies:
        results.append(
            CheckResult(
                id="proc.zombies",
                name="Zombie processes detected",
                description="Zombie processes found.",
                status="warn",
                severity="high",
                details="\n".join(zombies),
                plugin="process_tree",
            )
        )
    else:
        results.append(
            CheckResult(
                id="proc.zombies.none",
                name="No zombie processes",
                description="No zombie processes detected.",
                status="ok",
                severity="info",
                plugin="process_tree",
            )
        )

    # ------------------------------------------------------------
    # 2. Orphaned processes
    # ------------------------------------------------------------
    orphaned = _orphans(rows)

    if orphaned:
        results.append(
            CheckResult(
                id="proc.orphans",
                name="Orphaned processes detected",
                description="Processes whose parent does not exist.",
                status="warn",
                severity="medium",
                details="\n".join(orphaned),
                plugin="process_tree",
            )
        )
    else:
        results.append(
            CheckResult(
                id="proc.orphans.none",
                name="No orphaned processes",
                description="No orphaned processes detected.",
                status="ok",
                severity="info",
                plugin="process_tree",
            )
        )

    # ------------------------------------------------------------
    # 3. Exec-chain anomalies
    # ------------------------------------------------------------
    anomalies = []
    for r in rows:
        if r["cmd"].strip() == "":
            anomalies.append(r["pid"])

    if anomalies:
        results.append(
            CheckResult(
                id="proc.exec.anomalies",
                name="Exec-chain anomalies",
                description="Processes with empty or missing command lines.",
                status="warn",
                severity="low",
                details="\n".join(anomalies),
                plugin="process_tree",
            )
        )
    else:
        results.append(
            CheckResult(
                id="proc.exec.ok",
                name="Exec-chain normal",
                description="No exec-chain anomalies detected.",
                status="ok",
                severity="info",
                plugin="process_tree",
            )
        )

    return results
