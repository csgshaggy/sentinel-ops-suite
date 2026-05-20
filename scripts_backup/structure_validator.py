#!/usr/bin/env python
"""
Structure validator for SSRF Command Console.

Checks:
- Required directories and files exist.
- Package layout is correct.
- No obvious drift in critical metadata.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]


def check_exists(paths: Iterable[Path], label: str) -> bool:
    ok = True
    for p in paths:
        if not p.exists():
            print(f"[STRUCTURE] MISSING {label}: {p}")
            ok = False
        else:
            print(f"[STRUCTURE] OK {label}: {p}")
    return ok


def main() -> int:
    ok = True

    required_dirs = [
        ROOT / "src",
        ROOT / "src" / "ssrf_command_console",
        ROOT / "backend",
        ROOT / "frontend",
        ROOT / "config",
        ROOT / "docs",
    ]
    ok &= check_exists(required_dirs, "DIR")

    required_files = [
        ROOT / "pyproject.toml",
        ROOT / "Makefile",
        ROOT / "bootstrap.sh",
        ROOT / "LICENSE",
    ]
    ok &= check_exists(required_files, "FILE")

    # Package layout sanity
    pkg_init = ROOT / "src" / "ssrf_command_console" / "__init__.py"
    ok &= check_exists([pkg_init], "PKG_INIT")

    cli_file = ROOT / "src" / "ssrf_command_console" / "cli.py"
    ok &= check_exists([cli_file], "CLI_MODULE")

    plugins_dir = ROOT / "src" / "ssrf_command_console" / "plugins"
    ok &= check_exists([plugins_dir], "PLUGINS_DIR")

    # Duplicate pyproject.toml detection (drift)
    extra_pyprojects = list(ROOT.rglob("pyproject.toml"))
    extra_pyprojects = [p for p in extra_pyprojects if p != ROOT / "pyproject.toml"]
    if extra_pyprojects:
        ok = False
        print("[STRUCTURE] DRIFT: extra pyproject.toml files detected:")
        for p in extra_pyprojects:
            print(f"  - {p}")

    print("[STRUCTURE] RESULT:", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
