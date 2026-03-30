import json
from pathlib import Path
from datetime import datetime

ANOMALY_FILE = Path("anomalies.jsonl")
REPAIR_LOG = Path("repair_history.jsonl")

def run_repair():
    """
    Executes automated repair actions based on recent anomalies.
    """

    if not ANOMALY_FILE.exists():
        return {"status": "no_anomalies", "repairs": []}

    lines = ANOMALY_FILE.read_text().strip().split("\n")[-5:]
    anomalies = [json.loads(l) for l in lines]

    repairs = []

    for a in anomalies:
        if a["type"] == "low_score":
            repairs.append({
                "action": "restart_services",
                "message": "Restarting backend services due to low health score"
            })

        if a["type"] == "sudden_drop":
            repairs.append({
                "action": "clear_cache",
                "message": "Clearing cache due to sudden health drop"
            })

        if a["type"] == "negative_trend":
            repairs.append({
                "action": "rebuild_frontend",
                "message": "Rebuilding frontend due to negative health trend"
            })

    # Execute repairs (stubbed)
    for r in repairs:
        print(f"[REPAIR] {r['action']}: {r['message']}")

    # Log repairs
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "repairs": repairs,
        "anomalies": anomalies,
    }

    with REPAIR_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry
