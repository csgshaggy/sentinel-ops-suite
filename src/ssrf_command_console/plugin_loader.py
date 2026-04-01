"""
Plugin auto-loader for SSRF Command Console.

Loads plugins from the `plugins` package and exposes a registry.
Each plugin module is expected to define a `run()` callable.
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import Callable, Dict


def load_plugins() -> Dict[str, Callable]:
    import ssrf_command_console.plugins as plugins_pkg

    registry: Dict[str, Callable] = {}

    for module_info in pkgutil.iter_modules(plugins_pkg.__path__):
        name = module_info.name
        full_name = f"{plugins_pkg.__name__}.{name}"

        try:
            module = importlib.import_module(full_name)
        except Exception as exc:  # noqa: BLE001
            # Soft-fail: plugin is skipped but does not crash the CLI.
            print(f"[plugins] Failed to import {full_name}: {exc}")
            continue

        run_fn = getattr(module, "run", None)
        if callable(run_fn):
            registry[name] = run_fn
        else:
            print(f"[plugins] Skipping {full_name}: no callable 'run'")

    return registry
