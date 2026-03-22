#!/usr/bin/env python3
"""
Combined operator pipeline for structural integrity enforcement.

Steps:
1. Cleanup incorrect __init__.py files
2. Fix missing __init__.py files (safe)
3. Run SuperDoctor
4. Validate structure with dry-run
"""

import subprocess
import sys

def run_step(label, command):
    print(f"\n=== {label} ===")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ FAILED: {label}")
        sys.exit(result.returncode)

def main():
    run_step("Cleanup incorrect __init__.py files",
             "python tools/cleanup_bad_inits.py")

    run_step("Fix missing __init__.py files (safe)",
             "python tools/fix_missing_inits.py")

    run_step("Run SuperDoctor",
             "python tools/super_doctor.py")

    run_step("Validate structure (dry-run)",
             "python tools/super_doctor.py --dry-run")

    print("\n✔ All checks passed. Structure validated.")

if __name__ == "__main__":
    main()
