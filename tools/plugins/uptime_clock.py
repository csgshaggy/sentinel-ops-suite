"""
SuperDoctor Plugin: Uptime, Boot Time & Clock Sanity
Location: tools/plugins/uptime_clock.py

Checks:
- System uptime
- Boot time (best-effort)
- Clock skew detection
- Time source sanity (NTP hints)
- Cross-platform safe
"""

import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _uptime_seconds_posix() -> Optional[int]:
    """
    POSIX: read /proc/uptime.
    """
    try:
        with open("/proc/uptime") as f:
            return int(float(f.read().split()[0]))
    except Exception:
        return None


def _uptime_seconds_windows() -> Optional[int]:
    """
    Windows: use 'net stats srv' or 'wmic os get lastbootuptime'.
    """
    # Try WMIC first
    try:
        out = subprocess.check_output(
            ["wmic", "os", "get", "lastbootuptime"], text=True, errors="ignore"
        ).splitlines()
        for line in out:
            if line.strip() and "LastBootUpTime" not in line:
                # Format: YYYYMMDDHHMMSS.mmmmmms+timezone
                raw = line.strip().split(".")[0]
                boot = datetime.strptime(raw, "%Y%m%d%H%M%S")
                return int((datetime.now() - boot).total_seconds())
    except Exception:
        pass

    # Fallback: net stats srv
    try:
        out = subprocess.check_output(
            ["net", "stats", "srv"], text=True, errors="ignore"
        )
        for line in out.splitlines():
            if "Statistics since" in line:
                ts = line.split("since", 1)[1].strip()
                boot = datetime.strptime(ts, "%m/%d/%Y %I:%M:%S %p")
                return int((datetime.now() - boot).total_seconds())
    except Exception:
        pass

    return None


def _clock_skew() -> Optional[str]:
    """
    Best-effort clock skew detection using 'timedatectl' or Windows w32tm.
    """
    if os.name == "nt":
        try:
            out = subprocess.check_output(
                ["w32tm", "/query", "/status"], text=True, errors="ignore"
            )
            return out.strip()
        except Exception:
            return None

    # POSIX: timedatectl
    try:
        out = subprocess.check_output(["timedatectl"], text=True, errors="ignore")
        return out.strip()
    except Exception:
        return None


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. Uptime
    # ------------------------------------------------------------
    if os.name == "nt":
        uptime = _uptime_seconds_windows()
    else:
        uptime = _uptime_seconds_posix()

    if uptime is None:
        results.append(
            CheckResult(
                id="uptime.unavailable",
                name="Uptime unavailable",
                description="Could not determine system uptime.",
                status="warn",
                severity="medium",
                plugin="uptime_clock",
            )
        )
    else:
        human = str(timedelta(seconds=uptime))
        results.append(
            CheckResult(
                id="uptime.ok",
                name="System uptime",
                description="System uptime detected.",
                status="ok",
                severity="info",
                details=human,
                plugin="uptime_clock",
            )
        )

        if uptime < 300:
            results.append(
                CheckResult(
                    id="uptime.recent_boot",
                    name="Recent boot",
                    description="System booted within the last 5 minutes.",
                    status="warn",
                    severity="low",
                    plugin="uptime_clock",
                )
            )

    # ------------------------------------------------------------
    # 2. Clock skew / time source
    # ------------------------------------------------------------
    skew = _clock_skew()

    if skew:
        results.append(
            CheckResult(
                id="clock.skew",
                name="Clock / time source",
                description="Time source and clock information.",
                status="ok",
                severity="info",
                details=skew,
                plugin="uptime_clock",
            )
        )
    else:
        results.append(
            CheckResult(
                id="clock.skew.unavailable",
                name="Clock info unavailable",
                description="Could not retrieve clock or time-source information.",
                status="warn",
                severity="low",
                plugin="uptime_clock",
            )
        )

    return results
