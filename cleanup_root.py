#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "ssrf_console"
CONSOLE_DIR = PACKAGE_ROOT / "console"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# Operator / tooling scripts that must NEVER live inside the package
OPERATOR_SCRIPTS = {
    "doctor.py",
    "project_doctor.py",
    "cleanup_root.py",
    "auto_fix_missing_modules.py",
    "repair_encoding_and_clean.py",
    "validate_imports.py",
    "project_health.py",
    "auto_repair_structure.py",
    "fix_imports.py",
}


def header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def safe_mkdir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def delete_if_exists(path: Path):
    """Delete a file or directory safely, skipping non-writable items."""
    if not path.exists():
        return

    if not os.access(path, os.W_OK):
        print(f"[SKIP] Cannot delete (not writable): {path}")
        return

    print(f"[DELETE] {path}")

    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        try:
            path.unlink()
        except PermissionError:
            print(f"[SKIP] Permission denied while deleting file: {path}")


def move_if_exists(src: Path, dest: Path):
    """Move a file safely, skipping non-writable items."""
    if not src.exists():
        return

    if not os.access(src, os.W_OK):
        print(f"[SKIP] Cannot move (not writable): {src}")
        return

    safe_mkdir(dest.parent)
    print(f"[MOVE] {src} -> {dest}")

    try:
        shutil.move(str(src), str(dest))
    except PermissionError:
        print(f"[SKIP] Permission denied while moving: {src}")


def clean_package_of_operator_scripts():
    """Remove operator scripts that accidentally ended up inside the package."""
    print("[CHECK] Scanning for operator scripts inside package...")

    if not PACKAGE_ROOT.exists():
        return

    for py_file in PACKAGE_ROOT.rglob("*.py"):
        if py_file.name in OPERATOR_SCRIPTS:
            dest = PROJECT_ROOT / py_file.name
            print(f"[FIX] Operator script found inside package: {py_file}")
            print(f"      Moving back to root: {dest}")

            if os.access(py_file, os.W_OK):
                shutil.move(str(py_file), str(dest))
            else:
                print(f"[SKIP] Cannot move (not writable): {py_file}")


def clean_package_of_non_modules():
    """Warn and relocate any non-module files inside the package."""
    print("[CHECK] Scanning for non-module files inside package...")

    if not PACKAGE_ROOT.exists():
        return

    for item in PACKAGE_ROOT.rglob("*"):
        if item.is_dir():
            continue

        # Allowed: .py files only
        if item.suffix == ".py":
            continue

        print(f"[WARN] Non-module file found inside package: {item}")

        dest = SCRIPTS_DIR / item.name
        safe_mkdir(SCRIPTS_DIR)

        if os.access(item, os.W_OK):
            print(f"[MOVE] Moving to scripts/: {dest}")
            shutil.move(str(item), str(dest))
        else:
            print(f"[SKIP] Cannot move (not writable): {item}")


def warn_root_owned_files():
    """Warn about any root-owned files that may cause future issues."""
    print("[CHECK] Scanning for root-owned files...")

    for item in PROJECT_ROOT.rglob("*"):
        try:
            st = item.stat()
            if st.st_uid == 0:  # root-owned
                print(f"[WARN] Root-owned file detected: {item}")
        except Exception:
            continue


def main():
    header("ROOT CLEANUP STARTED")

    safe_mkdir(SCRIPTS_DIR)

    # 1. Delete debris files
    debris = [
        "autosync_test_file.txt",
        "autosync_test.txt",
        "test_autosync.txt",
    ]
    for f in debris:
        delete_if_exists(PROJECT_ROOT / f)

    # 2. Delete __pycache__ directories safely
    for pycache in PROJECT_ROOT.rglob("__pycache__"):
        delete_if_exists(pycache)

    # 3. Move operator scripts in root into scripts/
    for script in OPERATOR_SCRIPTS:
        if script in {"doctor.py", "cleanup_root.py"}:
            continue
        move_if_exists(PROJECT_ROOT / script, SCRIPTS_DIR / script)

    # 4. Move TUI health script into console package
    move_if_exists(PROJECT_ROOT / "tui_health.py", CONSOLE_DIR / "tui_health.py")

    # 5. Rename archive → legacy
    archive = PROJECT_ROOT / "archive"
    legacy = PROJECT_ROOT / "legacy"
    if archive.exists():
        print("[RENAME] archive -> legacy")
        shutil.move(str(archive), str(legacy))

    # 6. Eject operator scripts from package
    clean_package_of_operator_scripts()

    # 7. Eject non-module files from package
    clean_package_of_non_modules()

    # 8. Warn about root-owned files
    warn_root_owned_files()

    # 9. Warn about venv
    venv = PROJECT_ROOT / "venv"
    if venv.exists():
        print("[WARN] venv/ detected in project root.")
        print("       Best practice: move it outside the repo or delete & recreate.")

    # 10. Final tree
    header("FINAL PROJECT TREE")
    for path in sorted(PROJECT_ROOT.iterdir()):
        print(" -", path.name)

    header("CLEANUP COMPLETE")


if __name__ == "__main__":
    main()
