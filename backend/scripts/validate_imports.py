import os
import pkgutil
import importlib

PACKAGE = "app"

def walk_and_import(package):
    missing = []
    package_path = os.path.join(os.getcwd(), PACKAGE)

    print(f"Scanning package: {package_path}")

    for importer, modname, ispkg in pkgutil.walk_packages([package_path], prefix=f"{PACKAGE}."):
        try:
            importlib.import_module(modname)
        except ModuleNotFoundError as e:
            missing.append((modname, str(e)))
        except Exception as e:
            # Other errors (syntax, runtime) still indicate the module exists
            print(f"[WARN] {modname} exists but raised: {e}")

    return missing


if __name__ == "__main__":
    missing = walk_and_import(PACKAGE)

    if not missing:
        print("\n✔ All modules imported successfully — no missing files.")
    else:
        print("\n❌ Missing modules detected:")
        for mod, err in missing:
            print(f"  - {mod}: {err}")
