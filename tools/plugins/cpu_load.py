"""
SuperDoctor Plugin: CPU Load & Thermal Risk
Location: tools/plugins/cpu_load.py

Checks:
- CPU core count
- Load average (Linux/macOS)
- Windows CPU load (best-effort via WMIC)
- Thermal risk indicators (heuristic)
- High-load warnings
- Cross-platform safe
"""

import os
import subprocess
from typing import List, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _get_load_average() -> Optional[tuple]:
    """
    Returns (1m, 5m, 15m) load averages on POSIX systems.
    Windows returns None.
    """
    if os.name == "nt":
        return None
    try:
        return os.getloadavg()
    except Exception:
        return None


def _get_windows_cpu_load() -> Optional[float]:
    """
    Best-effort CPU load detection on Windows using WMIC.
    Returns a percentage or None.
    """
    try:
        out = subprocess.check_output(
            ["wmic", "cpu", "get", "loadpercentage"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        for line in out.splitlines():
            line = line.strip()
            if line.isdigit():
                return float(line)
    except Exception:
        pass
    return None


def _thermal_risk(load: float, cores: int) -> str:
    """
    Heuristic thermal risk indicator.
    """
    if cores <= 0:
        return "unknown"

    per_core = load / cores

    if per_core >= 1.5:
        return "critical"
    if per_core >= 1.0:
        return "high"
    if per_core >= 0.7:
        return "moderate"
    return "low"


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root=None) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # 1. CPU core count
    # ------------------------------------------------------------
    cores = os.cpu_count() or 1

    results.append(
        CheckResult(
            id="cpu.cores",
            name="CPU core count",
            description="Detected number of CPU cores.",
            status="ok",
            severity="info",
            details=str(cores),
            plugin="cpu_load",
        )
    )

    # ------------------------------------------------------------
    # 2. Load average (POSIX)
    # ------------------------------------------------------------
    loadavg = _get_load_average()

    if loadavg is not None:
        one, five, fifteen = loadavg

        results.append(
            CheckResult(
                id="cpu.loadavg",
                name="Load average",
                description="POSIX load average (1m, 5m, 15m).",
                status="ok",
                severity="info",
                details=f"1m={one:.2f}, 5m={five:.2f}, 15m={fifteen:.2f}",
                plugin="cpu_load",
            )
        )

        # High load warnings
        risk = _thermal_risk(one, cores)

        if risk == "critical":
            results.append(
                CheckResult(
                    id="cpu.load.critical",
                    name="Critical CPU load",
                    description="CPU load is critically high.",
                    status="fail",
                    severity="critical",
                    plugin="cpu_load",
                )
            )
        elif risk == "high":
            results.append(
                CheckResult(
                    id="cpu.load.high",
                    name="High CPU load",
                    description="CPU load is high and may cause throttling.",
                    status="warn",
                    severity="high",
                    plugin="cpu_load",
                )
            )
        elif risk == "moderate":
            results.append(
                CheckResult(
                    id="cpu.load.moderate",
                    name="Moderate CPU load",
                    description="CPU load is moderate.",
                    status="warn",
                    severity="medium",
                    plugin="cpu_load",
                )
            )
        else:
            results.append(
                CheckResult(
                    id="cpu.load.low",
                    name="Low CPU load",
                    description="CPU load is within normal range.",
                    status="ok",
                    severity="info",
                    plugin="cpu_load",
                )
            )

    # ------------------------------------------------------------
    # 3. Windows CPU load
    # ------------------------------------------------------------
    if os.name == "nt":
        win_load = _get_windows_cpu_load()
        if win_load is None:
            results.append(
                CheckResult(
                    id="cpu.winload.unavailable",
                    name="Windows CPU load unavailable",
                    description="Could not retrieve CPU load via WMIC.",
                    status="warn",
                    severity="low",
                    plugin="cpu_load",
                )
            )
        else:
            results.append(
                CheckResult(
                    id="cpu.winload",
                    name="Windows CPU load",
                    description="CPU load percentage from WMIC.",
                    status="ok",
                    severity="info",
                    details=f"{win_load:.1f}%",
                    plugin="cpu_load",
                )
            )

            # High load warnings
            if win_load >= 95:
                results.append(
                    CheckResult(
                        id="cpu.winload.critical",
                        name="Critical CPU load (Windows)",
                        description="CPU load is critically high.",
                        status="fail",
                        severity="critical",
                        plugin="cpu_load",
                    )
                )
            elif win_load >= 80:
                results.append(
                    CheckResult(
                        id="cpu.winload.high",
                        name="High CPU load (Windows)",
                        description="CPU load is high and may cause throttling.",
                        status="warn",
                        severity="high",
                        plugin="cpu_load",
                    )
                )
            elif win_load >= 60:
                results.append(
                    CheckResult(
                        id="cpu.winload.moderate",
                        name="Moderate CPU load (Windows)",
                        description="CPU load is moderate.",
                        status="warn",
                        severity="medium",
                        plugin="cpu_load",
                    )
                )
            else:
                results.append(
                    CheckResult(
                        id="cpu.winload.low",
                        name="Low CPU load (Windows)",
                        description="CPU load is within normal range.",
                        status="ok",
                        severity="info",
                        plugin="cpu_load",
                    )
                )

    return results
