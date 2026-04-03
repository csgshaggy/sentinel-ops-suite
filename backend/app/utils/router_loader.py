import importlib
import pkgutil
from fastapi import APIRouter


def auto_discover_routers():
    """
    Safely discovers routers inside app/routers/.
    Only modules containing a 'router' attribute are loaded.
    """
    discovered = []

    for _, module_name, _ in pkgutil.iter_modules(["app/routers"]):
        module_path = f"app.routers.{module_name}"

        try:
            module = importlib.import_module(module_path)

            if hasattr(module, "router") and isinstance(module.router, APIRouter):
                discovered.append((module_name, module.router))
            else:
                print(f"  - Skipped {module_name}: no valid router")

        except Exception as exc:
            print(f"  - Failed to import {module_name}: {exc}")

    return discovered
