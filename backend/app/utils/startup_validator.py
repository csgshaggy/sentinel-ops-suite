import importlib
import pkgutil
import sys
from pathlib import Path


def validate_backend_startup():
    print("\n=== Sentinel Ops Backend Startup Validator ===")

    # ------------------------------------------------------------
    # 1. Python Path Inspection
    # ------------------------------------------------------------
    print("\n[PYTHON PATH]")
    for p in sys.path:
        print(f"  - {p}")

    # ------------------------------------------------------------
    # 2. Detect Shadowed 'app' Packages
    # ------------------------------------------------------------
    print("\n[PACKAGE SHADOW CHECK]")
    app_paths = list(Path(".").rglob("app/__init__.py"))
    if len(app_paths) > 1:
        print("  ⚠ WARNING: Multiple 'app/' packages detected:")
        for ap in app_paths:
            print(f"    - {ap}")
    else:
        print("  ✓ No shadowed app packages detected")

    # ------------------------------------------------------------
    # 3. Router Discovery Summary
    # ------------------------------------------------------------
    print("\n[ROUTER DISCOVERY]")
    router_modules = []
    for _, module_name, _ in pkgutil.iter_modules(["app/routers"]):
        if module_name.endswith("_router") or module_name in [
            "ci_summary", "git_snapshots", "idrim_router", "logs_router",
            "makefile_admin", "makefile_diff", "makefile_health",
            "ops_stream_router", "pelm", "pelm_stream", "plugins",
            "repo_health", "router_drift", "system", "workflow_runs"
        ]:
            router_modules.append(module_name)

    for mod in router_modules:
        try:
            importlib.import_module(f"app.routers.{mod}")
            print(f"  ✓ Loaded router: {mod}")
        except Exception as exc:
            print(f"  ✗ Failed to load router {mod}: {exc}")

    print("\n=== Startup Validation Complete ===\n")
