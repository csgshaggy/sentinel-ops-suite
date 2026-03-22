#!/usr/bin/env python3
import subprocess
import sys

GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
RESET = "\033[0m"

def run(cmd, label):
    print(f"{YELLOW}[CHECK]{RESET} {label}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"{RED}[FAIL]{RESET} {label}")
        return False
    print(f"{GREEN}[OK]{RESET} {label}")
    return True

def main():
    ok = True

    ok &= run("python3 scripts/project_tree_validator.py", "Project tree validator")
    ok &= run("python3 scripts/makefile_doctor.py", "Makefile duplicate target check")
    ok &= run("python3 scripts/import_validator.py", "Import validator (if present)")

    if ok:
        print(f"{GREEN}Repo integrity: PASS{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}Repo integrity: FAIL{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
