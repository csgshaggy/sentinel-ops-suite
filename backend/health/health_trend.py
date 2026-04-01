import json
from pathlib import Path
from backend.health.health_score import compute_health_score

TREND_FILE = Path("data/health_trend.json")
TREND_FILE.parent.mkdir(exist_ok=True)

def load_trend():
    if not TREND_FILE.exists():
        return []
    try:
        return json.loads(TREND_FILE.read_text())
    except Exception:
        return []

def append_score():
    trend = load_trend()
    score = compute_health_score()
    trend.append(score)
    TREND_FILE.write_text(json.dumps(trend, indent=2))
    return score

def get_trend():
    return load_trend()
