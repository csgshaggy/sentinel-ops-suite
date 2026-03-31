import json
from datetime import datetime
from pathlib import Path

ANOMALY_FILE = Path("anomalies.jsonl")
REPAIR_LOG = Path("repair_history.jsonl")


def run_repair():
    """
    Executes automated repair actions based on recent anomalies.
    """

    if not ANOMALY_FILE.exists():
        return {"status": "no_anomalies", "repairs": []}

    lines = ANOMALY_FILE.read_text().strip().split("\n")[-5:]
    anomalies = [json.loads(line) for line in lines]

    repairs = []

    for anomaly in anomalies:
        anomaly_type = anomaly.get("type")

        if anomaly_type == "low_score":
            repairs.append(
                {
                    "action": "restart_services",
                    "message": "Restarting backend services due to low health score",
                }
            )

        if anomaly_type == "sudden_drop":
            repairs.append(
                {
                    "action": "clear_cache",
                    "message": "Clearing cache due to sudden health drop",
                }
            )

        if anomaly_type == "negative_trend":
            repairs.append(
                {
                    "action": "rebuild_frontend",
                    "message": "Rebuilding frontend due to negative health trend",
                }
            )

    # Execute repairs (stubbed)
    for repair in repairs:
        print(f"[REPAIR] {repair['action']}: {repair['message']}")

    # Log repairs
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "repairs": repairs,
        "anomalies": anomalies,
    }

    with REPAIR_LOG.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")

    return entry
