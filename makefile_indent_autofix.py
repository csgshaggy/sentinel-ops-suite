#!/usr/bin/env python3
import sys
from pathlib import Path

MAKEFILE = Path("Makefile")

def is_command_line(prev_line: str) -> bool:
    """
    Heuristic: a line is a command if the previous non-empty,
    non-comment line looks like a target (ends with ':').
    """
    prev = prev_line.strip()
    if not prev or prev.startswith("#"):
        return False
    return prev.endswith(":")

def main() -> int:
    if not MAKEFILE.exists():
        print("Makefile not found", file=sys.stderr)
        return 1

    lines = MAKEFILE.read_text(encoding="utf-8").splitlines(keepends=True)
    fixed = []
    prev_nonempty = ""

    for line in lines:
        stripped = line.rstrip("\n")

        # Track previous non-empty, non-comment line
        if stripped.strip() and not stripped.lstrip().startswith("#"):
            candidate_prev = stripped
        else:
            candidate_prev = prev_nonempty

        # If line starts with spaces and previous line is a target -> convert to TAB
        if line.startswith(" ") and is_command_line(prev_nonempty):
            new_line = "\t" + line.lstrip()
            fixed.append(new_line)
        else:
            fixed.append(line)

        if stripped.strip() and not stripped.lstrip().startswith("#"):
            prev_nonempty = candidate_prev

    backup = MAKEFILE.with_suffix(".bak")
    backup.write_text("".join(lines), encoding="utf-8")
    MAKEFILE.write_text("".join(fixed), encoding="utf-8")

    print(f"✔ Makefile indentation auto‑fixed (backup at {backup})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
