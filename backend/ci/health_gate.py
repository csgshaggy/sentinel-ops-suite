import sys
from backend.health.health_trend import load_trend
from backend.alerts.alert_engine import evaluate_alerts

THRESHOLD_SCORE = 60

def main():
    trend = load_trend()
    if not trend:
        print("[ci-health] No trend data available — cannot evaluate.")
        sys.exit(1)

    latest = trend[-1]
    alerts = evaluate_alerts()

    # ---------------------------------------------------------
    # Gate 1: Health score threshold
    # ---------------------------------------------------------
    if latest["score"] < THRESHOLD_SCORE:
        print(f"[ci-health] FAIL: Health score {latest['score']} < {THRESHOLD_SCORE}")
        sys.exit(1)

    # ---------------------------------------------------------
    # Gate 2: Active alerts
    # ---------------------------------------------------------
    if alerts:
        print("[ci-health] FAIL: Active alerts detected:")
        for a in alerts:
            print(f" - {a['type']}: {a['message']}")
        sys.exit(1)

    print("[ci-health] PASS: System health OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
