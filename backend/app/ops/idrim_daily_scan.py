"""
IDRIM Daily Scan
----------------
Runs a daily IDRIM analysis using the unified IDRIM engine + service layer.

This script is designed to be:
- cron/systemd friendly
- deterministic
- operator-grade
- drift-free
"""

import json
from datetime import datetime
    IDRIMService,
    IDRIMRequest,
)

service = IDRIMService()


def log(msg: str):
    """Operator-grade timestamped logging."""
    ts = datetime.utcnow().isoformat()
    print(f"[IDRIM-DailyScan] {ts} | {msg}")


def run_daily_scan():
    log("Starting daily IDRIM scan...")

    # Load baseline
    baseline = service.load_baseline()
    if baseline is None:
        log("No baseline found. Daily scan aborted.")
        return

    log("Baseline loaded successfully.")

    # Build request
    req = IDRIMRequest(
        source="daily_scan",
        scope="scheduled",
        payload=baseline,
    )

    # Run analysis
    try:
        result = service.run_analysis(req)
        service.save_last_result(result)

        log("Analysis complete.")
        log(f"Integrity Score: {result.integrity_score}")
        log(f"Drift Summary: {json.dumps(result.drift, indent=2)}")

    except Exception as exc:
        log(f"ERROR during daily scan: {exc}")
        return

    log("Daily IDRIM scan finished successfully.")


if __name__ == "__main__":
    run_daily_scan()
