import importlib
import pkgutil
import traceback
from pathlib import Path

# -----------------------------------------
# PROJECT ROOT (hard‑pointed for reliability)
# -----------------------------------------
PROJECT_ROOT = Path.home() / "ssrf-command-console"
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE = "ssrf_console"

def validate_imports():
    print(f"[OK] Project root: {PROJECT_ROOT}")
    print(f"[OK] SRC root: {SRC_ROOT}")
    print(f"[OK] Validating package: {PACKAGE}\n")

    # Ensure src/ssrf_console exists
    package_path = SRC_ROOT / PACKAGE
    if not package_path.exists():
        print(f"[FAIL] Package root not found: {package_path}")
        return

    failed = []

    # Walk all modules under src/ssrf_console
    for module in pkgutil.walk_packages([str(package_path)], f"{PACKAGE}."):
        name = module.name
        print(f"[TEST] Importing {name} ... ", end="")
        try:
            importlib.import_module(name)
            print("OK")
        except Exception:
            print("FAIL")
            failed.append((name, traceback.format_exc()))

    # Summary
    print("\n=== Import Validation Summary ===")
    print(f"[!] {len(failed)} module(s) failed to import:\n")

    for name, tb in failed:
        print(f"--- {name} ---")
        print(tb)

if __name__ == "__main__":
    validate_imports()
