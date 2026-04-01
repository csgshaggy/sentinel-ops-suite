# tools/validators/makefile_drift_detector.py

import sys
from pathlib import Path
import difflib

CANONICAL_PATH = Path("tools/validators/canonical_makefile.txt")
MAKEFILE_PATH = Path("Makefile")


def load(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text().splitlines(keepends=True)


def main() -> int:
    if not CANONICAL_PATH.exists():
        print("Canonical Makefile not found:", CANONICAL_PATH, file=sys.stderr)
        return 1

    if not MAKEFILE_PATH.exists():
        print("Makefile not found:", file=sys.stderr)
        return 1

    canonical = load(CANONICAL_PATH)
    current = load(MAKEFILE_PATH)

    diff = list(difflib.unified_diff(
        canonical,
        current,
        fromfile="canonical_makefile",
        tofile="Makefile",
    ))

    if diff:
        print("Makefile drift detected:")
        for line in diff:
            print(line, end="")
        return 1

    print("Makefile drift detector: no drift detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
