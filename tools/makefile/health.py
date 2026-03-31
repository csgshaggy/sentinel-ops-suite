from __future__ import annotations

from typing import Any, Dict

from .drift_detector import detect_drift
from .linter import lint_makefile
from .version_check import check_version


def compute_health(json_mode: bool = False) -> Dict[str, Any]:
    drift = detect_drift()
    lint = lint_makefile()
    version = check_version()

    score = 100

    if drift["drift"]:
        score -= 40

    if not lint["ok"]:
        score -= 30

    if not version["found"]:
        score -= 30

    score = max(score, 0)

    result = {
        "health_score": score,
        "drift": drift["drift"],
        "lint_ok": lint["ok"],
        "version_found": version["found"],
    }

    if json_mode:
        import json

        print(json.dumps(result, indent=2))

    return result
