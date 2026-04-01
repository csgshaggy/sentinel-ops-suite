# backend/app/anomaly_engine.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .anomaly_detector import detect_anomalies
from .sync_history import load_sync_history

ANOMALY_LOG = Path("health_history.jsonl")


def _write_anomaly_record(record: Dict[str, Any]) -> None:
    """Append a single anomaly record to the persistent JSONL log."""
    ANOMALY_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ANOMALY_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _load_anomaly_log() -> List[Dict[str, Any]]:
    """Load all anomaly records from the JSONL log."""
    if not ANOMALY_LOG.exists():
        return []
    with ANOMALY_LOG.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def run_anomaly_engine() -> Dict[str, Any]:
    """
    Execute the anomaly engine:
    - Load sync history
    - Run anomaly detection
    - Persist anomalies
    - Return structured results
    """
    history = load_sync_history()
    anomalies = detect_anomalies(history)

    timestamp = datetime.utcnow().isoformat()

    for anomaly in anomalies:
        record = {
            "timestamp": timestamp,
            "type": anomaly.get("type"),
            "severity": anomaly.get("severity"),
            "details": anomaly.get("details"),
        }
        _write_anomaly_record(record)

    return {
        "timestamp": timestamp,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
        "history_length": len(history),
    }


def load_anomaly_history() -> List[Dict[str, Any]]:
    """Return all persisted anomaly records."""
    return _load_anomaly_log()
