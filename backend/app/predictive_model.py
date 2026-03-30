import json
from pathlib import Path
import numpy as np

HISTORY_FILE = Path("health_history.jsonl")

def predict_health(n_future: int = 5):
    """
    Predicts future health scores using simple linear regression.
    ML-lite, no external dependencies.
    """

    if not HISTORY_FILE.exists():
        return {"predictions": []}

    lines = HISTORY_FILE.read_text().strip().split("\n")[-30:]
    history = [json.loads(l) for l in lines]

    if len(history) < 3:
        return {"predictions": []}

    scores = np.array([h["score"] for h in history])
    x = np.arange(len(scores))

    # Linear regression
    m, b = np.polyfit(x, scores, 1)

    future = []
    for i in range(1, n_future + 1):
        future.append(float(m * (len(scores) + i) + b))

    return {
        "trend_slope": float(m),
        "predictions": future,
        "last_score": scores[-1],
    }
