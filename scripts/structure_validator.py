#!/usr/bin/env python3
"""
Operator‑Grade Structure Validator for SSRF Command Console

This script enforces deterministic project layout rules for CI and
local development. Any violation produces a non‑zero exit code with
forensic‑grade output.
"""

import sys
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
PKG = SRC / "ssrf_command_console"
REQUIRED_FILES = [
    ROOT / "pyproject.toml",
    ROOT / "README.md",
    PKG / "__init__.py",
    PKG / "cli.py",
]


def fail(msg: str):
    print(f"[FAIL] {msg}")
    sys.exit(1)


def ok(msg: str):
    print(f"[OK] {msg}")


def check_paths():
    if not SRC.exists():
        fail(f"Missing src/ directory at: {SRC}")

    if not PKG.exists():
        fail(f"Missing package directory: {PKG}")

    ok("Source tree exists and is correctly structured.")


def check_required_files():
    for f in REQUIRED_FILES:
        if not f.exists():
            fail(f"Missing required file: {f}")
    ok("All required files are present.")


def check_cli_entrypoint():
    cli_file = PKG / "cli.py"
    if not cli_file.exists():
        fail("cli.py missing — cannot validate entrypoint.")

    try:
        mod = importlib.import_module("ssrf_command_console.cli")
    except Exception as e:
        fail(f"Import error in CLI module: {e}")

    if not hasattr(mod, "cli"):
        fail("CLI entrypoint missing: expected attribute `cli` in cli.py")

    ok("CLI entrypoint resolved successfully.")


def main():
    print("=== SSRF Command Console — Structure Validation ===")

    check_paths()
    check_required_files()
    check_cli_entrypoint()

    print("\nAll structure checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
