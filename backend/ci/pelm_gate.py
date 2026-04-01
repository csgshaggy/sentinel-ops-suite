import sys

from backend.pelm.pelm_tools import detect_pelm_drift, detect_pelm_regression


def main():
    drift = detect_pelm_drift()
    if drift["drift"]:
        print("[pelm-gate] FAIL: PELM drift detected")
        if drift["diff"]:
            print(drift["diff"])
        sys.exit(1)

    regression = detect_pelm_regression()
    if regression["regression"]:
        print("[pelm-gate] FAIL: PELM regression detected")
        print(regression)
        sys.exit(1)

    print("[pelm-gate] PASS: PELM stable")
    sys.exit(0)


if __name__ == "__main__":
    main()
