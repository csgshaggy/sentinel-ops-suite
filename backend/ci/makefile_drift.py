import sys
from backend.ci.makefile_tools import detect_drift

def main():
    result = detect_drift()
    if not result["drift"]:
        print("[makefile-drift] No drift detected.")
        sys.exit(0)

    print("[makefile-drift] DRIFT DETECTED:")
    print(result["diff"] or "(no diff content)")
    sys.exit(1)

if __name__ == "__main__":
    main()
