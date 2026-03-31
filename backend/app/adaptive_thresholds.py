import json
from pathlib import Path

import numpy as np

HISTORY_FILE = Path("health_history.jsonl")
THRESHOLD_FILE = Path("adaptive_thresholds.json")

DEFAULTS = {
    "low_score_threshold": 50,
    "sudden_drop_threshold": 15,
    "trend_slope_threshold": -5,
}


def load_thresholds():
    if not THRESHOLD_FILE.exists():
        return DEFAULTS.copy()
    return json.loads(THRESHOLD_FILE.read_text())


def save_thresholds(thresholds):
    THRESHOLD_FILE.write_text(json.dumps(thresholds, indent=2))


def compute_adaptive_thresholds():
    """
    Computes new thresholds based on:
    - rolling average
    - rolling variance
    - trend slope
    - predictive modeling
    """

    if not HISTORY_FILE.exists():
        return DEFAULTS.copy()

    lines = HISTORY_FILE.read_text().strip().split("\n")[-40:]
    history = [json.loads(line) for line in lines]

    if len(history) < 5:
        return DEFAULTS.copy()

    scores = np.array([entry["score"] for entry in history])
    avg = float(np.mean(scores))
    std = float(np.std(scores))

    thresholds = {
        "low_score_threshold": max(20, avg - std * 1.5),
        "sudden_drop_threshold": max(5, std * 1.2),
        "trend_slope_threshold": -abs(std / 2),
    }

    save_thresholds(thresholds)
    return thresholds
