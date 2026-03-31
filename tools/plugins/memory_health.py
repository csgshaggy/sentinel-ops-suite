"""
SuperDoctor Plugin: Memory Health & Pressure Detection
Location: tools/plugins/memory_health.py

Checks:
- Total + available RAM
- Swap usage (Linux/macOS)
- Windows memory load (best-effort)
- Memory pressure heuristics
- Low-memory warnings
- Cross-platform safe
"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _read_meminfo() -> Optional[dict]:
    """
    Parse /proc/meminfo on Linux.
    Returns dict of key → kB.
    """
    meminfo = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if ":" in line:
                    key, val = line.split(":", 1)
                    meminfo[key.strip()] = int(val.strip().split()[0])
        return meminfo
    except Exception:
        return None


def _windows_memory_load() -> Optional[int]:
    """
    Best-effort Windows memory load percentage via WMIC.
    """
    try:
        out = subprocess.check_output(
            [
                "wmic",
                "OS",
                "get",
                "FreePhysicalMemory,TotalVisibleMemorySize",
                "/Value",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        free = None
        total = None
        for line in out.splitlines():
            if "FreePhysicalMemory" in line:
                free = int(line.split("=")[1])
            elif "TotalVisibleMemorySize" in line:
                total = int(line.split("=")[1])
        if free is not None and total is not None and total > 0:
            used_pct = 100 - ((free / total) * 100)
            return int(used_pct)
    except Exception:
        pass
    return None


def _format_mb(kb: int) -> str:
    return f"{kb / 1024:.1f} MB"


def _pressure_level(used_pct: float) -> str:
    """
    Heuristic memory pressure classification.
    """
    if used_pct >= 95:
        return "critical"
    if used_pct >= 85:
        return "high"
    if used_pct >= 70:
        return "moderate"
    return "low"


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    # ------------------------------------------------------------
    # POSIX memory detection
    # ------------------------------------------------------------
    if os.name != "nt":
        meminfo = _read_meminfo()

        if meminfo is None:
            results.append(
                CheckResult(
                    id="mem.unavailable",
                    name="Memory info unavailable",
                    description="Could not read /proc/meminfo.",
                    status="warn",
                    severity="medium",
                    plugin="memory_health",
                )
            )
            return results

        total = meminfo.get("MemTotal", 0)
        free = meminfo.get("MemAvailable", meminfo.get("MemFree", 0))
        used = total - free
        used_pct = (used / total) * 100 if total > 0 else 0

        results.append(
            CheckResult(
                id="mem.summary",
                name="Memory usage",
                description="Detected RAM usage.",
                status="ok",
                severity="info",
                details=(
                    f"Total: {_format_mb(total)}\n"
                    f"Used:  {_format_mb(used)} ({used_pct:.1f}%)\n"
                    f"Free:  {_format_mb(free)}"
                ),
                plugin="memory_health",
            )
        )

        # Pressure classification
        pressure = _pressure_level(used_pct)

        if pressure == "critical":
            results.append(
                CheckResult(
                    id="mem.pressure.critical",
                    name="Critical memory pressure",
                    description="System memory is critically low.",
                    status="fail",
                    severity="critical",
                    plugin="memory_health",
                )
            )
        elif pressure == "high":
            results.append(
                CheckResult(
                    id="mem.pressure.high",
                    name="High memory pressure",
                    description="System memory is heavily used.",
                    status="warn",
                    severity="high",
                    plugin="memory_health",
                )
            )
        elif pressure == "moderate":
            results.append(
                CheckResult(
                    id="mem.pressure.moderate",
                    name="Moderate memory pressure",
                    description="System memory usage is elevated.",
                    status="warn",
                    severity="medium",
                    plugin="memory_health",
                )
            )
        else:
            results.append(
                CheckResult(
                    id="mem.pressure.low",
                    name="Low memory pressure",
                    description="Memory usage is within normal range.",
                    status="ok",
                    severity="info",
                    plugin="memory_health",
                )
            )

        # Swap detection
        swap_total = meminfo.get("SwapTotal", 0)
        swap_free = meminfo.get("SwapFree", 0)
        swap_used = swap_total - swap_free

        if swap_total > 0:
            results.append(
                CheckResult(
                    id="mem.swap",
                    name="Swap usage",
                    description="Swap memory usage.",
                    status="ok",
                    severity="info",
                    details=(
                        f"Total: {_format_mb(swap_total)}\n"
                        f"Used:  {_format_mb(swap_used)}"
                    ),
                    plugin="memory_health",
                )
            )

    # ------------------------------------------------------------
    # Windows memory detection
    # ------------------------------------------------------------
    else:
        used_pct = _windows_memory_load()

        if used_pct is None:
            results.append(
                CheckResult(
                    id="mem.win.unavailable",
                    name="Windows memory info unavailable",
                    description="Could not retrieve memory usage via WMIC.",
                    status="warn",
                    severity="medium",
                    plugin="memory_health",
                )
            )
            return results

        results.append(
            CheckResult(
                id="mem.win.summary",
                name="Memory usage (Windows)",
                description="Detected RAM usage.",
                status="ok",
                severity="info",
                details=f"Used: {used_pct:.1f}%",
                plugin="memory_health",
            )
        )

        pressure = _pressure_level(used_pct)

        if pressure == "critical":
            results.append(
                CheckResult(
                    id="mem.win.critical",
                    name="Critical memory pressure",
                    description="System memory is critically low.",
                    status="fail",
                    severity="critical",
                    plugin="memory_health",
                )
            )
        elif pressure == "high":
            results.append(
                CheckResult(
                    id="mem.win.high",
                    name="High memory pressure",
                    description="System memory is heavily used.",
                    status="warn",
                    severity="high",
                    plugin="memory_health",
                )
            )
        elif pressure == "moderate":
            results.append(
                CheckResult(
                    id="mem.win.moderate",
                    name="Moderate memory pressure",
                    description="System memory usage is elevated.",
                    status="warn",
                    severity="medium",
                    plugin="memory_health",
                )
            )
        else:
            results.append(
                CheckResult(
                    id="mem.win.low",
                    name="Low memory pressure",
                    description="Memory usage is within normal range.",
                    status="ok",
                    severity="info",
                    plugin="memory_health",
                )
            )

    return results
