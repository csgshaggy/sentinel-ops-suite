#!/usr/bin/env python3
import sys
from pathlib import Path

REQUIRED_PYTHON = (3, 10)
REQUIRED_PACKAGES = [
    "rich",
    "fastapi",
    "uvicorn",
    "httpx",
]


def check_python_version():
    if sys.version_info < REQUIRED_PYTHON:
        print(
            f"[FAIL] Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+ required, "
            f"found {sys.version.split()[0]}"
        )
        return False
    print(f"[OK] Python version: {sys.version.split()[0]}")
    return True


def check_packages():
    ok = True
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
            print(f"[OK] Package available: {pkg}")
        except ImportError:
            print(f"[FAIL] Missing package: {pkg}")
            ok = False
    return ok


def check_project_root():
    here = Path(__file__).resolve()
    root = here.parent.parent
    src = root / "src"
    if not src.exists():
        print(f"[WARN] src/ directory not found at {src}")
        return False
    print(f"[OK] Project root: {root}")
    return True


def main():
    print("=== SSRF Console Preflight Check ===")
    ok = True
    ok &= check_python_version()
    ok &= check_packages()
    ok &= check_project_root()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
