# tools/validators/makefile_self_heal.py

import sys
from pathlib import Path

MAKEFILE_PATH = Path("Makefile")
CANONICAL_PATH = Path("tools/validators/canonical_makefile.txt")


def load(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text().splitlines(keepends=True)


def write(path: Path, lines: list[str]):
    path.write_text("".join(lines))


def main() -> int:
    if not MAKEFILE_PATH.exists():
        print("Self-heal: Makefile missing — cannot repair.", file=sys.stderr)
        return 1

    if not CANONICAL_PATH.exists():
        print("Self-heal: canonical Makefile missing:", CANONICAL_PATH, file=sys.stderr)
        return 1

    current = load(MAKEFILE_PATH)
    canonical = load(CANONICAL_PATH)

    # If identical → nothing to heal
    if current == canonical:
        print("Self-heal: Makefile already matches canonical version.")
        return 0

    # Strategy:
    # 1. Identify missing lines
    # 2. Append them to the end of the Makefile
    # 3. Do NOT remove or overwrite user modifications
    missing_lines = []
    for line in canonical:
        if line not in current:
            missing_lines.append(line)

    if not missing_lines:
        print("Self-heal: No missing lines detected.")
        return 0

    print("Self-heal: Repairing Makefile by appending missing canonical lines...")

    repaired = current + ["\n# --- SELF-HEAL PATCH BELOW ---\n"] + missing_lines
    write(MAKEFILE_PATH, repaired)

    print("Self-heal: Makefile repaired successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
