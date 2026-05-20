"""
Plugin loader and validator for SSRF Command Console.

- Uses the explicit PLUGIN_REGISTRY from tools.plugins
- Validates that each plugin:
  - imports successfully
  - exposes PLUGIN_INFO
  - has a callable entrypoint defined in PLUGIN_INFO["entrypoint"]

Used by:
- make heal (structure validation step)
- Super Doctor (plugin registry health)
"""

from __future__ import annotations

import importlib
import traceback
from typing import Any, Callable, Dict

PLUGIN_PACKAGE = "tools.plugins"


class PluginLoadError(Exception):
    """Raised when a plugin cannot be loaded or validated."""


def list_plugins() -> list[str]:
    """
    Return the list of plugin names from the explicit registry.

    This is deterministic and CI-safe: only plugins explicitly registered
    in tools.plugins.PLUGIN_REGISTRY are considered.
    """
    from tools.plugins import PLUGIN_REGISTRY

    return list(PLUGIN_REGISTRY.keys())


def load_plugin_module(name: str):
    """
    Import a plugin module by name from the PLUGIN_PACKAGE.
    """
    full_name = f"{PLUGIN_PACKAGE}.{name}"
    return importlib.import_module(full_name)


def get_plugin_entrypoint(module) -> Callable[..., Any]:
    """
    Resolve the plugin entrypoint from PLUGIN_INFO.

    Requirements:
    - module.PLUGIN_INFO exists
    - module.PLUGIN_INFO["entrypoint"] exists
    - getattr(module, entrypoint) is callable
    """
    if not hasattr(module, "PLUGIN_INFO"):
        raise PluginLoadError(f"Plugin {module.__name__} missing PLUGIN_INFO")

    info = getattr(module, "PLUGIN_INFO")
    if not isinstance(info, dict):
        raise PluginLoadError(f"Plugin {module.__name__} PLUGIN_INFO must be a dict")

    entry_name = info.get("entrypoint")
    if not entry_name:
        raise PluginLoadError(
            f"Plugin {module.__name__} missing entrypoint in PLUGIN_INFO"
        )

    entry = getattr(module, entry_name, None)
    if not callable(entry):
        raise PluginLoadError("Entrypoint is not callable")

    return entry


def validate_plugins() -> Dict[str, Dict[str, Any]]:
    """
    Validate all plugins in the explicit registry.

    Returns:
        {
            "good_plugins": {name: {"module": module, "entry": entry}},
            "bad_plugins": {name: "<traceback string>"},
        }

    This structure is consumed by Super Doctor to render the Plugin Registry
    section and by the structure validation step in make heal.
    """
    good_plugins: Dict[str, Dict[str, Any]] = {}
    bad_plugins: Dict[str, str] = {}

    for name in list_plugins():
        try:
            module = load_plugin_module(name)
            entry = get_plugin_entrypoint(module)
            good_plugins[name] = {"module": module, "entry": entry}
        except Exception:
            tb = traceback.format_exc()
            bad_plugins[name] = tb
            print(f"\n[ERROR] {name}")
            print(tb)

    print("\nValidation complete.")
    return {"good_plugins": good_plugins, "bad_plugins": bad_plugins}


def main() -> None:
    """
    CLI entrypoint: python -m tools.plugin_loader

    Runs validation and prints results. Does not exit non-zero on failure,
    so that make heal can continue while still surfacing plugin issues.
    """
    results = validate_plugins()

    # Minimal summary for human/Doctor consumption.
    bad = results["bad_plugins"]
    if bad:
        print("\nPlugin validation completed with errors.")
        print(f"Bad plugins: {', '.join(sorted(bad.keys()))}")
    else:
        print("\nAll plugins validated successfully.")


if __name__ == "__main__":
    main()
