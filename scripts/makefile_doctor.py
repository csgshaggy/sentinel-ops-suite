#!/usr/bin/env python3
import re
import sys

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
RESET = "\033[0m"

TARGET_PATTERN = re.compile(r"^([a-zA-Z0-9\-_]+):")

def main():
    try:
        with open("Makefile", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"{RED}[FAIL]{RESET} No Makefile found in current directory.")
        sys.exit(1)

    targets = {}
    duplicates = {}

    for i, line in enumerate(lines):
        match = TARGET_PATTERN.match(line)
        if match:
            target = match.group(1)
            if target in targets:
                duplicates.setdefault(target, []).append(i + 1)
            else:
                targets[target] = i + 1

    if duplicates:
        print(f"{RED}[DUPLICATES FOUND]{RESET}")
        for target, lines in duplicates.items():
            print(f"  Target '{target}' defined multiple times at lines: {targets[target]}, {', '.join(map(str, lines))}")
        sys.exit(1)

    print(f"{GREEN}[OK]{RESET} No duplicate Makefile targets detected.")

if __name__ == "__main__":
    main()
