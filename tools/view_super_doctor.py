import json
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path.home() / "ssrf-command-console"
LOG_PATH = PROJECT_ROOT / "runtime" / "super_doctor_report.json"


def load_report():
    if not LOG_PATH.exists():
        print(f"[FAIL] Report not found: {LOG_PATH}")
        return []
    with LOG_PATH.open() as f:
        return json.load(f)


def print_summary(entries):
    counts = Counter(e["severity"] for e in entries)
    print("\n=== Super Doctor Summary ===")
    for level in ["FAIL", "WARN", "INFO"]:
        print(f"{level}: {counts.get(level, 0)}")


def print_entries(entries, severity=None):
    print("\n=== Super Doctor Entries ===")
    for e in entries:
        if severity and e["severity"] != severity:
            continue
        print(f"[{e['severity']}] {e['message']}")


def main():
    entries = load_report()
    if not entries:
        return

    print_summary(entries)

    print("\nFilter options:")
    print("  1) All")
    print("  2) FAIL only")
    print("  3) WARN only")
    print("  4) INFO only")
    choice = input("\nSelect filter (1-4): ").strip()

    severity = None
    if choice == "2":
        severity = "FAIL"
    elif choice == "3":
        severity = "WARN"
    elif choice == "4":
        severity = "INFO"

    print_entries(entries, severity)


if __name__ == "__main__":
    main()
