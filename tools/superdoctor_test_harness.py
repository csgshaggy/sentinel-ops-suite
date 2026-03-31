#!/usr/bin/env python3
"""
SuperDoctor Plugin Test Harness
Path: ssrf-command-console/tools/superdoctor_test_harness.py

Discovers plugins, validates importability, and runs SuperDoctor in test mode.
"""

import importlib
import json
import pkgutil
from pathlib import Path

from tools.super_doctor import run_super_doctor

ROOT = Path(__file__).resolve().parents[1]
PLUGINS_DIR = ROOT / "tools" / "plugins"


def discover_plugins():
    """Yield (module_name, module_object or exception)."""
    package_name = "tools.plugins"

    for module in pkgutil.iter_modules([str(PLUGINS_DIR)]):
        mod_name = f"{package_name}.{module.name}"
        try:
            mod = importlib.import_module(mod_name)
            yield mod_name, mod
        except Exception as e:
            yield mod_name, e


def main():
    print("=== SuperDoctor Plugin Test Harness ===")
    print(f"Root: {ROOT}")
    print(f"Plugins directory: {PLUGINS_DIR}")

    print("\n=== Discovering Plugins ===")
    for mod_name, result in discover_plugins():
        if isinstance(result, Exception):
            print(f" - {mod_name}: IMPORT FAILED -> {result}")
        else:
            print(f" - {mod_name}: OK")

    print("\n=== Running SuperDoctor (test mode) ===")
    try:
        result = run_super_doctor()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"SuperDoctor execution failed: {e}")
        raise


if __name__ == "__main__":
    main()
