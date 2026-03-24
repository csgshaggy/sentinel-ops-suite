from __future__ import annotations

import difflib
import os
from typing import Dict, List


# ------------------------------------------------------------
# ANSI color helpers
# ------------------------------------------------------------

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def _read_file_safe(path: str) -> List[str]:
    """
    Safely read a file and return its lines.
    Returns an empty list if the file cannot be read.
    """
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception:
        return []


def _colorize_diff(diff: List[str]) -> List[str]:
    """
    Apply ANSI colors to unified diff output.
    """
    colored: List[str] = []

    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            colored.append(f"{GREEN}{line}{RESET}")
        elif line.startswith("-") and not line.startswith("---"):
            colored.append(f"{RED}{line}{RESET}")
        elif line.startswith("@@"):
            colored.append(f"{YELLOW}{line}{RESET}")
        else:
            colored.append(line)

    return colored


def generate_diff(
    old_path: str, new_path: str, color: bool = True
) -> Dict[str, List[str]]:
    """
    Generate a unified diff between two documentation files.
    """
    old_lines = _read_file_safe(old_path)
    new_lines = _read_file_safe(new_path)

    diff = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=old_path,
            tofile=new_path,
            lineterm="",
        )
    )

    if color:
        diff = _colorize_diff(diff)

    return {
        "old_file": old_path,
        "new_file": new_path,
        "diff": diff,
        "changed": len(diff) > 0,
    }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Generate a diff between two documentation files."
    )
    parser.add_argument("old", help="Path to old file")
    parser.add_argument("new", help="Path to new file")
    parser.add_argument(
        "--no-color", action="store_true", help="Disable ANSI color output"
    )

    args = parser.parse_args()

    result = generate_diff(args.old, args.new, color=not args.no_color)
    print(json.dumps(result, indent=2))
