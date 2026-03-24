from __future__ import annotations

from typing import Any, Dict, List

from tools.super_doctor import run_super_doctor
from tools.makefile_drift_detector import detect_drift
from tools.makefile_health import compute_health
from tools.makefile_linter import lint_makefile
from tools.makefile_version_check import check_version
from tools.plugin_registry_viewer import list_plugins


def detect_anomalies() -> Dict[str, Any]:
    anomalies: List[str] = []

    doctor = run_super_doctor({})
    doctor_health = doctor.get("summary", {}).get("health_score", 0)
    if doctor_health < 90:
        anomalies.append(f"Doctor health below threshold: {doctor_health}")

    drift = detect_drift()
    if drift["drift"]:
        anomalies.append("Makefile drift detected")

    mf_health = compute_health()
    if mf_health["health_score"] < 90:
        anomalies.append(
            f"Makefile health below threshold: {mf_health['health_score']}"
        )

    lint = lint_makefile()
    if not lint["ok"]:
        anomalies.append("Makefile linter reported issues")

    version = check_version()
    if not version.get("found"):
        anomalies.append("Makefile version stamp missing")

    plugins = list_plugins({})
    if not plugins:
        anomalies.append("No plugins registered")

    return {
        "anomalies": anomalies,
        "ok": len(anomalies) == 0,
    }
