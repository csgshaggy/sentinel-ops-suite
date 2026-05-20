#!/usr/bin/env python3
import sys
from pathlib import Path

MAKEFILE = Path("Makefile")


def main() -> int:
    if not MAKEFILE.exists():
        print("Makefile not found", file=sys.stderr)
        return 1

    bad_lines = []
    with MAKEFILE.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            # Ignore blank lines and comments
            if not line.strip() or line.lstrip().startswith("#"):
                continue

            # Commands must start with TAB if they are indented
            if line.startswith(" "):  # leading spaces
                bad_lines.append((idx, line.rstrip("\n")))
            # Disallow mixed indent: TAB followed by spaces at start
            elif line.startswith("\t "):
                bad_lines.append((idx, line.rstrip("\n")))

    if bad_lines:
        print("❌ Makefile indentation violations detected:")
        for ln, content in bad_lines:
            print(f"  Line {ln}: {content}")
        print("\nCommands must be indented with a single TAB, not spaces.")
        return 1

    print("✔ Makefile indentation is clean (TAB‑only for commands).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
