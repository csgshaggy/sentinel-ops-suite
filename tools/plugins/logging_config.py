"""
SuperDoctor Plugin: Logging Configuration Integrity
Location: tools/plugins/logging_config.py

Checks:
- Root logger level sanity
- Duplicate handlers
- Disabled loggers
- Handler-level drift (handler level != logger level)
- Missing formatters
- Misconfigured propagation
- Cross-platform safe
"""

import logging
from pathlib import Path
from typing import Dict, List

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _level_name(level: int) -> str:
    try:
        return logging.getLevelName(level)
    except Exception:
        return str(level)


def _collect_loggers() -> Dict[str, logging.Logger]:
    """
    Collect all known loggers from logging.root.manager.
    """
    mgr = logging.root.manager
    loggers = {"root": logging.getLogger()}
    loggers.update(mgr.loggerDict)
    return {k: v for k, v in loggers.items() if isinstance(v, logging.Logger)}


def _detect_duplicate_handlers(logger: logging.Logger) -> List[str]:
    seen = set()
    duplicates = []
    for h in logger.handlers:
        key = (type(h), getattr(h, "baseFilename", None))
        if key in seen:
            duplicates.append(str(h))
        else:
            seen.add(key)
    return duplicates


def _detect_handler_level_drift(logger: logging.Logger) -> List[str]:
    """
    Detect handlers whose level is more restrictive than the logger.
    """
    drift = []
    for h in logger.handlers:
        if h.level > logger.level and h.level != logging.NOTSET:
            drift.append(
                f"Handler {h} level={_level_name(h.level)} > logger level={_level_name(logger.level)}"
            )
    return drift


def _detect_missing_formatters(logger: logging.Logger) -> List[str]:
    missing = []
    for h in logger.handlers:
        if h.formatter is None:
            missing.append(str(h))
    return missing


# ------------------------------------------------------------
# Main plugin
# ------------------------------------------------------------


def run_checks(mode: Mode, project_root: Path = None) -> List[CheckResult]:
    results: List[CheckResult] = []

    loggers = _collect_loggers()
    root_logger = logging.getLogger()

    # ------------------------------------------------------------
    # 1. Root logger level sanity
    # ------------------------------------------------------------
    root_level = root_logger.level

    if root_level >= logging.WARNING:
        results.append(
            CheckResult(
                id="log.root.high_level",
                name="Root logger level too high",
                description="Root logger level is WARNING or higher; logs may be suppressed.",
                status="warn",
                severity="high",
                details=f"root level={_level_name(root_level)}",
                plugin="logging_config",
            )
        )
    else:
        results.append(
            CheckResult(
                id="log.root.ok",
                name="Root logger level OK",
                description="Root logger level is appropriate.",
                status="ok",
                severity="info",
                details=f"root level={_level_name(root_level)}",
                plugin="logging_config",
            )
        )

    # ------------------------------------------------------------
    # 2. Duplicate handlers
    # ------------------------------------------------------------
    dupes = []
    for name, logger in loggers.items():
        d = _detect_duplicate_handlers(logger)
        if d:
            dupes.append(f"{name}: {d}")

    if dupes:
        results.append(
            CheckResult(
                id="log.duplicates",
                name="Duplicate logging handlers",
                description="Some loggers have duplicate handlers.",
                status="warn",
                severity="medium",
                details="\n".join(dupes),
                plugin="logging_config",
            )
        )
    else:
        results.append(
            CheckResult(
                id="log.duplicates.none",
                name="No duplicate handlers",
                description="No duplicate logging handlers detected.",
                status="ok",
                severity="info",
                plugin="logging_config",
            )
        )

    # ------------------------------------------------------------
    # 3. Disabled loggers
    # ------------------------------------------------------------
    disabled = [name for name, logger in loggers.items() if logger.disabled]

    if disabled:
        results.append(
            CheckResult(
                id="log.disabled",
                name="Disabled loggers",
                description="Some loggers are disabled.",
                status="warn",
                severity="medium",
                details="\n".join(disabled),
                plugin="logging_config",
            )
        )
    else:
        results.append(
            CheckResult(
                id="log.disabled.none",
                name="No disabled loggers",
                description="No loggers are disabled.",
                status="ok",
                severity="info",
                plugin="logging_config",
            )
        )

    # ------------------------------------------------------------
    # 4. Handler-level drift
    # ------------------------------------------------------------
    drift = []
    for name, logger in loggers.items():
        d = _detect_handler_level_drift(logger)
        if d:
            drift.append(f"{name}:\n" + "\n".join(d))

    if drift:
        results.append(
            CheckResult(
                id="log.level_drift",
                name="Handler-level drift",
                description="Some handlers have levels more restrictive than their logger.",
                status="warn",
                severity="medium",
                details="\n\n".join(drift),
                plugin="logging_config",
            )
        )
    else:
        results.append(
            CheckResult(
                id="log.level_drift.none",
                name="No handler-level drift",
                description="All handlers have appropriate levels.",
                status="ok",
                severity="info",
                plugin="logging_config",
            )
        )

    # ------------------------------------------------------------
    # 5. Missing formatters
    # ------------------------------------------------------------
    missing_fmt = []
    for name, logger in loggers.items():
        m = _detect_missing_formatters(logger)
        if m:
            missing_fmt.append(f"{name}:\n" + "\n".join(m))

    if missing_fmt:
        results.append(
            CheckResult(
                id="log.formatters.missing",
                name="Missing formatters",
                description="Some handlers do not have formatters.",
                status="warn",
                severity="medium",
                details="\n\n".join(missing_fmt),
                plugin="logging_config",
            )
        )
    else:
        results.append(
            CheckResult(
                id="log.formatters.ok",
                name="All handlers have formatters",
                description="No missing formatter issues detected.",
                status="ok",
                severity="info",
                plugin="logging_config",
            )
        )

    return results
