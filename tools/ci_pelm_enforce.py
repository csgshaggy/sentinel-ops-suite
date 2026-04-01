#!/usr/bin/env python3
import sys
import json
import urllib.request

# ------------------------------------------------------------
# Thresholds (tune as needed)
# ------------------------------------------------------------
MAX_REGRESSION_SCORE = 40
MAX_RISK_ACCELERATION = 1
FAIL_ON_DRIFT = True

API_URL = "http://localhost:8000/pelm/regression"


def fail(msg):
    print(f"[CI-PELM-FAIL] {msg}")
    sys.exit(1)


def main():
    print("[CI] Fetching PELM regression analytics...")

    try:
        with urllib.request.urlopen(API_URL) as r:
            data = json.loads(r.read().decode())
    except Exception as e:
        fail(f"Unable to fetch regression data: {e}")

    regression_score = data.get("regression_score", 0)
    drift_detected = data.get("drift_detected", False)
    risk_acceleration = data.get("risk_acceleration", 0)

    print(json.dumps(data, indent=2))

    # --------------------------------------------------------
    # Enforcement Rules
    # --------------------------------------------------------

    if regression_score > MAX_REGRESSION_SCORE:
        fail(
            f"Regression score {regression_score} exceeds threshold "
            f"{MAX_REGRESSION_SCORE}"
        )

    if FAIL_ON_DRIFT and drift_detected:
        fail("Snapshot drift detected — CI enforcement triggered.")

    if risk_acceleration > MAX_RISK_ACCELERATION:
        fail(
            f"Risk acceleration {risk_acceleration} exceeds threshold "
            f"{MAX_RISK_ACCELERATION}"
        )

    print("[CI] PELM regression check passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
