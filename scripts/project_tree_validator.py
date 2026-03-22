#!/usr/bin/env python3
import os
import sys

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
RESET = "\033[0m"

REQUIRED_DIRS = [
    "scripts",
    "tools",
    "tools/plugins",
    "backend",
]

REQUIRED_FILES = [
    "Makefile",
    ".superdoctor_mode",
]

def fail(msg):
    print(f"{RED}[FAIL]{RESET} {msg}")
    sys.exit(1)

def ok(msg):
    print(f"{GREEN}[OK]{RESET} {msg}")

def warn(msg):
    print(f"{YELLOW}[WARN]{RESET} {msg}")

def main():
    root = os.getcwd()
    print(f"{YELLOW}Validating project tree at: {root}{RESET}")

    # Check Makefile location
    if not os.path.exists("Makefile"):
        fail("Makefile not found in project root. It MUST reside at the top level.")

    ok("Makefile found in correct location.")

    # Check required directories
    for d in REQUIRED_DIRS:
        if not os.path.isdir(d):
            warn(f"Missing directory: {d}")
        else:
            ok(f"Directory exists: {d}")

    # Check required files
    for f in REQUIRED_FILES:
        if not os.path.isfile(f):
            warn(f"Missing file: {f}")
        else:
            ok(f"File exists: {f}")

    print(f"{GREEN}Project tree validation complete.{RESET}")

if __name__ == "__main__":
    main()
