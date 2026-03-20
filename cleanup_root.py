#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / "ssrf_console"
CONSOLE_DIR = PACKAGE_ROOT / "console"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def safe_mkdir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def delete_if_exists(path: Path):
    if path.exists():
        print(f"[DELETE] {path}")
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def move_if_exists(src: Path, dest: Path):
    if src.exists():
        safe_mkdir(dest.parent)
        print(f"[MOVE] {src} -> {dest}")
        shutil.move(str(src), str(dest))


def main():
    header("ROOT CLEANUP STARTED")

    # Ensure scripts directory exists
    safe_mkdir(SCRIPTS_DIR)

    # 1. Delete debris files
    debris = [
        "autosync_test_file.txt",
        "autosync_test.txt",
        "test_autosync.txt",
    ]
    for f in debris:
        delete_if_exists(PROJECT_ROOT / f)

    # 2. Delete __pycache__ directories
    for pycache in PROJECT_ROOT.rglob("__pycache__"):
        delete_if_exists(pycache)

    # 3. Move operator scripts into scripts/
    operator_scripts = [
        "auto_fix_missing_modules.py",
        "repair_encoding_and_clean.py",
        "validate_imports.py",
        "project_health.py",
    ]
    for script in operator_scripts:
        move_if_exists(PROJECT_ROOT / script, SCRIPTS_DIR / script)

    # 4. Move TUI health script into console package
    move_if_exists(PROJECT_ROOT / "tui_health.py", CONSOLE_DIR / "tui_health.py")

    # 5. Rename archive → legacy
    archive = PROJECT_ROOT / "archive"
    legacy = PROJECT_ROOT / "legacy"
    if archive.exists():
        print(f"[RENAME] archive -> legacy")
        shutil.move(str(archive), str(legacy))

    # 6. Warn about venv
    venv = PROJECT_ROOT / "venv"
    if venv.exists():
        print("[WARN] venv/ detected in project root.")
        print("       Best practice: move it outside the repo or delete & recreate.")

    # 7. Print final tree
    header("FINAL PROJECT TREE")
    for path in sorted(PROJECT_ROOT.iterdir()):
        print(" -", path.name)

    header("CLEANUP COMPLETE")


if __name__ == "__main__":
    main()
