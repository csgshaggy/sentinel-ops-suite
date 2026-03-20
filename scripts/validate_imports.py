#!/usr/bin/env python3
import importlib
import pkgutil
import sys
import traceback
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_NAME = "ssrf_console"
PACKAGE_ROOT = SRC_ROOT / PACKAGE_NAME


def ensure_sys_path():
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))


def iter_modules(package_root: Path, package_name: str):
    """Yield full module names under a given package."""
    for module_info in pkgutil.walk_packages(
        [str(package_root)], prefix=f"{package_name}."
    ):
        yield module_info.name


def validate_imports():
    ensure_sys_path()

    if not PACKAGE_ROOT.exists():
        print(f"[FAIL] Package root not found: {PACKAGE_ROOT}")
        sys.exit(1)

    print(f"[OK] Using SRC root: {SRC_ROOT}")
    print(f"[OK] Validating package: {PACKAGE_NAME}")
    print("")

    failures = []

    for module_name in sorted(iter_modules(PACKAGE_ROOT, PACKAGE_NAME)):
        print(f"[TEST] Importing {module_name} ... ", end="", flush=True)
        try:
            importlib.import_module(module_name)
            print("OK")
        except Exception as e:
            print("FAIL")
            failures.append((module_name, e, traceback.format_exc()))

    print("\n=== Import Validation Summary ===")
    if not failures:
        print("[+] All modules imported successfully.")
        return 0

    print(f"[!] {len(failures)} module(s) failed to import:\n")
    for module_name, exc, tb in failures:
        print(f"--- {module_name} ---")
        print(f"Error: {exc}")
        print(tb)
        print("")

    return 1


def main():
    rc = validate_imports()
    sys.exit(rc)


if __name__ == "__main__":
    main()
