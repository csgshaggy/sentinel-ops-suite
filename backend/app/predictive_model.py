import json
from pathlib import Path

import numpy as np

HISTORY_FILE = Path("health_history.jsonl")


def predict_health(n_future: int = 5):
    """
    Predict future health scores using simple linear regression.
    ML-lite, no external dependencies.
    """

    if not HISTORY_FILE.exists():
        return {"predictions": []}

    lines = HISTORY_FILE.read_text().strip().split("\n")[-30:]
    history = [json.loads(line) for line in lines]

    if len(history) < 3:
        return {"predictions": []}

    scores = np.array([entry["score"] for entry in history])
    x = np.arange(len(scores))

    # Linear regression (slope m, intercept b)
    m, b = np.polyfit(x, scores, 1)

    future_predictions = [
        float(m * (len(scores) + i) + b) for i in range(1, n_future + 1)
    ]

    return {
        "trend_slope": float(m),
        "predictions": future_predictions,
        "last_score": scores[-1],
    }
