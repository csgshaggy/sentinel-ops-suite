#!/usr/bin/env python3
"""
Sentinel Ops — Full Backend Preflight Validator

Run BEFORE starting Uvicorn/systemd:

    PYTHONPATH=. python3 scripts/preflight_validate.py
"""

import os
import sys
import pkgutil
import importlib
import inspect
from pathlib import Path
from typing import List, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
ENV_FILE = BASE_DIR / ".env"

CRITICAL_ENV_VARS = [
    "DATABASE_URL",
    "JWT_SECRET_KEY",
    "SESSION_SECRET",
    "AWS_S3_BUCKET",
    "AWS_REGION",
]

CRITICAL_DEPENDENCIES = [
    "boto3",
    "botocore",
    "sqlalchemy",
    "fastapi",
    "uvicorn",
    "pydantic",
]

ROUTER_IMPORT_PREFIX = "from app.routers"
SERVICE_IMPORT_PREFIX = "from app.services"
MODEL_IMPORT_PREFIX = "from app.models"


def add_pythonpath():
    sys.path.append(str(BASE_DIR))


def load_env() -> dict:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()
    return env


def check_env_vars(env: dict) -> List[str]:
    missing = []
    for key in CRITICAL_ENV_VARS:
        if key not in env and not os.getenv(key):
            missing.append(key)
    return missing


def check_dependencies() -> List[str]:
    missing = []
    for dep in CRITICAL_DEPENDENCIES:
        try:
            importlib.import_module(dep)
        except Exception as e:
            missing.append(f"{dep} ({e})")
    return missing


def parse_import_targets(file_path: Path, prefix: str) -> List[Tuple[str, int]]:
    targets = []
    for i, line in enumerate(file_path.read_text().splitlines(), start=1):
        line = line.strip()
        if line.startswith(prefix):
            # e.g. from app.routers.settings import router as settings_router
            parts = line.split()
            if len(parts) >= 4 and parts[0] == "from":
                module = parts[1]
                targets.append((module, i))
    return targets


def module_to_path(module: str) -> Path:
    """
    app.routers.settings -> app/routers/settings.py
    """
    parts = module.split(".")
    if parts[0] != "app":
        return Path()
    return APP_DIR.joinpath(*parts[1:]).with_suffix(".py")


def check_router_service_model_structure() -> List[str]:
    issues = []

    main_py = APP_DIR / "main.py"
    if not main_py.exists():
        issues.append("Missing app/main.py")
        return issues

    # 1) Routers referenced in main.py
    router_imports = parse_import_targets(main_py, ROUTER_IMPORT_PREFIX)
    for module, line_no in router_imports:
        path = module_to_path(module)
        if not path.exists():
            issues.append(
                f"Router module {module} referenced in main.py:{line_no} "
                f"but file {path} does not exist"
            )

    # 2) Services referenced in routers
    for router_file in (APP_DIR / "routers").glob("*.py"):
        service_imports = parse_import_targets(router_file, SERVICE_IMPORT_PREFIX)
        for module, line_no in service_imports:
            path = module_to_path(module)
            if not path.exists():
                issues.append(
                    f"Service module {module} referenced in {router_file.relative_to(APP_DIR)}:{line_no} "
                    f"but file {path} does not exist"
                )

    # 3) Models referenced in services
    services_dir = APP_DIR / "services"
    if services_dir.exists():
        for service_file in services_dir.glob("*.py"):
            model_imports = parse_import_targets(service_file, MODEL_IMPORT_PREFIX)
            for module, line_no in model_imports:
                path = module_to_path(module)
                if not path.exists():
                    issues.append(
                        f"Model module {module} referenced in {service_file.relative_to(APP_DIR)}:{line_no} "
                        f"but file {path} does not exist"
                    )

    return issues


def walk_and_import_app() -> List[Tuple[str, str]]:
    missing = []
    print(f"[INFO] Import graph validation for package: {APP_DIR}")

    for importer, modname, ispkg in pkgutil.walk_packages([str(APP_DIR)], prefix="app."):
        try:
            importlib.import_module(modname)
        except Exception as e:
            missing.append((modname, repr(e)))
    return missing


def check_runtime_s3_client() -> List[str]:
    """
    Try importing s3_client and creating a client lazily if possible.
    This catches boto3/botocore runtime issues before Uvicorn.
    """
    issues = []
    try:
        s3_mod = importlib.import_module("app.services.s3_client")
    except ModuleNotFoundError:
        # S3 is optional; only warn if avatar_service exists
        avatar_path = APP_DIR / "services" / "avatar_service.py"
        if avatar_path.exists():
            issues.append(
                "app.services.s3_client missing but avatar_service.py exists "
                "(S3 avatar upload may fail)."
            )
        return issues
    except Exception as e:
        issues.append(f"Failed to import app.services.s3_client: {e}")
        return issues

    # Try to detect a lazy getter
    getter = None
    for name, obj in inspect.getmembers(s3_mod):
        if name.startswith("get_s3_client") and callable(obj):
            getter = obj
            break

    if getter is None:
        # Fall back to attribute named s3
        if hasattr(s3_mod, "s3"):
            # Accessing it may trigger boto3 client creation
            try:
                _ = getattr(s3_mod, "s3")
            except Exception as e:
                issues.append(f"S3 client initialization failed: {e}")
        else:
            issues.append(
                "app.services.s3_client has no get_s3_client() or s3 attribute; "
                "S3 integration may be misconfigured."
            )
    else:
        try:
            client = getter()
            # Optionally, check basic attributes
            _ = client.meta.service_model.service_name
        except Exception as e:
            issues.append(f"S3 client lazy initialization failed: {e}")

    return issues


def main():
    add_pythonpath()

    print("=== Sentinel Ops Backend Preflight Validator ===\n")

    env = load_env()
    env_missing = check_env_vars(env)
    deps_missing = check_dependencies()
    structure_issues = check_router_service_model_structure()
    import_failures = walk_and_import_app()
    s3_issues = check_runtime_s3_client()

    any_failures = False

    if env_missing:
        any_failures = True
        print("\n[ENV] Missing critical environment variables:")
        for key in env_missing:
            print(f"  - {key}")

    if deps_missing:
        any_failures = True
        print("\n[DEPS] Missing or broken Python dependencies:")
        for dep in deps_missing:
            print(f"  - {dep}")

    if structure_issues:
        any_failures = True
        print("\n[STRUCTURE] Router/Service/Model structure issues:")
        for issue in structure_issues:
            print(f"  - {issue}")

    if import_failures:
        any_failures = True
        print("\n[IMPORTS] Import graph failures in app package:")
        for mod, err in import_failures:
            print(f"  - {mod}: {err}")

    if s3_issues:
        any_failures = True
        print("\n[S3] S3 client/runtime issues:")
        for issue in s3_issues:
            print(f"  - {issue}")

    if not any_failures:
        print("\n✔ Preflight passed — backend is structurally and runtime‑ready.")
        sys.exit(0)
    else:
        print("\n❌ Preflight failed — see sections above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
