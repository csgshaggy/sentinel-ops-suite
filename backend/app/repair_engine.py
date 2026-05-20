from pathlib import Path
import sys
import difflib


ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = ROOT / "data"
MAKEFILE = ROOT / "Makefile"
MAKEFILE_SNAPSHOT = SNAPSHOT_DIR / "Makefile.snapshot"


def snapshot_repo() -> int:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    if MAKEFILE.exists():
        MAKEFILE_SNAPSHOT.write_text(MAKEFILE.read_text())
        print("[snapshot] Makefile snapshot updated.")
    else:
        print("[snapshot] Makefile not found.", file=sys.stderr)
        return 1
    return 0


def check_drift() -> int:
    if not MAKEFILE.exists() or not MAKEFILE_SNAPSHOT.exists():
        print("[drift] Makefile or snapshot missing.", file=sys.stderr)
        return 1

    current = MAKEFILE.read_text().splitlines()
    baseline = MAKEFILE_SNAPSHOT.read_text().splitlines()
    diff = list(difflib.unified_diff(baseline, current, fromfile="snapshot", tofile="Makefile"))

    if not diff:
        print("[drift] No Makefile drift detected.")
        return 0

    print("[drift] Makefile drift detected:")
    for line in diff:
        print(line)
    return 1


def heal_makefile() -> int:
    if not MAKEFILE_SNAPSHOT.exists():
        print("[heal] No Makefile snapshot found.", file=sys.stderr)
        return 1
    MAKEFILE.write_text(MAKEFILE_SNAPSHOT.read_text())
    print("[heal] Makefile restored from snapshot.")
    return 0


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True)
    args = parser.parse_args()

    if args.mode == "snapshot":
        sys.exit(snapshot_repo())
    elif args.mode == "drift":
        sys.exit(check_drift())
    elif args.mode == "makefile-heal":
        sys.exit(heal_makefile())
    else:
        print(f"Unknown mode: {args.mode}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
