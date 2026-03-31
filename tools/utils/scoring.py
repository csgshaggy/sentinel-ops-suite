"""
SuperDoctor Health Scoring Engine
Location: tools/utils/scoring.py

Computes a 0–100 health score based on:
- check severity
- check status (ok/warn/fail/skip)
- run mode (strict/balanced)

The scoring model is intentionally simple and stable.
"""

from typing import List

from tools.super_doctor import CheckResult
from utils.modes import Mode

# ------------------------------------------------------------
# Severity weights
# ------------------------------------------------------------

SEVERITY_WEIGHTS = {
    "info": 1,
    "low": 2,
    "medium": 4,
    "high": 7,
    "critical": 10,
}

# Status multipliers
STATUS_MULTIPLIER = {
    "ok": 0,
    "warn": 0.5,
    "fail": 1.0,
    "skip": 0.2,  # skipped checks still reduce confidence slightly
}


# ------------------------------------------------------------
# Core scoring logic
# ------------------------------------------------------------


def compute_health_score(results: List[CheckResult], mode: Mode) -> int:
    """
    Compute a 0–100 health score.

    Formula:
        score = 100 - penalty

    Penalty is based on:
        severity_weight * status_multiplier

    Mode adjustments:
        strict   → penalties × 1.2
        balanced → penalties × 1.0
    """
    penalty = 0.0

    for r in results:
        sev = SEVERITY_WEIGHTS.get(r.severity, 3)
        mult = STATUS_MULTIPLIER.get(r.status, 0.5)
        penalty += sev * mult

    # Mode scaling
    if mode == Mode.STRICT:
        penalty *= 1.2

    # Clamp score
    score = max(0, min(100, int(100 - penalty)))
    return score
