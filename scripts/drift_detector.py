#!/usr/bin/env python3
import os
import json
import hashlib
import sys
from pathlib import Path

BASELINE_FILE = "runtime/structure_baseline.json"
DRIFT_OUTPUT = "runtime/structure_drift.json"


# ------------------------------------------------------------
# FILE HASHING
# ------------------------------------------------------------
def hash_file(path: str) -> str:
    """Return SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# ------------------------------------------------------------
# TREE WALKER
# ------------------------------------------------------------
def walk_tree(root="."):
    """
    Walk the project tree and return a structure map:
    {
        "path": {
            "dirs": [...],
            "files": { "file.py": "<hash>" }
        }
    }
    """
    structure = {}

    for dirpath, dirs, files in os.walk(root):
        # Skip irrelevant directories
        if any([
            dirpath.startswith("./venv"),
            dirpath.startswith("./.git"),
            dirpath.startswith("./__pycache__"),
        ]):
            continue

        rel = os.path.relpath(dirpath, root)

        structure[rel] = {
            "dirs": sorted(dirs),
            "files": {f: hash_file(os.path.join(dirpath, f)) for f in files}
        }

    return structure


# ------------------------------------------------------------
# BASELINE LOAD/SAVE
# ------------------------------------------------------------
def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        return None
    with open(BASELINE_FILE, "r") as f:
        return json.load(f)


def save_baseline(structure):
    os.makedirs("runtime", exist_ok=True)
    with open(BASELINE_FILE, "w") as f:
        json.dump(structure, f, indent=2)


# ------------------------------------------------------------
# DRIFT COMPARISON
# ------------------------------------------------------------
def compare(baseline, current):
    drift = {
        "new_paths": [],
        "missing_paths": [],
        "modified_files": [],
    }

    baseline_paths = set(baseline.keys())
    current_paths = set(current.keys())

    # New directories or file paths
    drift["new_paths"] = sorted(list(current_paths - baseline_paths))

    # Missing directories or file paths
    drift["missing_paths"] = sorted(list(baseline_paths - current_paths))

    # Compare shared paths
    for path in baseline_paths & current_paths:
        base_files = baseline[path]["files"]
        curr_files = current[path]["files"]

        # Missing files
        for f in base_files:
            if f not in curr_files:
                drift["missing_paths"].append(f"{path}/{f}")
            elif base_files[f] != curr_files[f]:
                drift["modified_files"].append(f"{path}/{f}")

        # New files
        for f in curr_files:
            if f not in base_files:
                drift["new_paths"].append(f"{path}/{f}")

    return drift


# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------
def main():
    os.makedirs("runtime", exist_ok=True)

    # Handle baseline generation mode
    if "--generate-baseline" in sys.argv:
        current = walk_tree()
        save_baseline(current)
        print("[+] Baseline regenerated.")
        return

    # Normal drift detection mode
    current = walk_tree()
    baseline = load_baseline()

    if baseline is None:
        print("[!] No baseline found. Creating one now.")
        save_baseline(current)
        print("[+] Baseline created at runtime/structure_baseline.json")
        return

    drift = compare(baseline, current)

    print("\n=== STRUCTURE DRIFT REPORT ===\n")

    if drift["new_paths"]:
        print("🟩 New paths:")
        for p in drift["new_paths"]:
            print(f"  + {p}")

    if drift["missing_paths"]:
        print("\n🟥 Missing paths:")
        for p in drift["missing_paths"]:
            print(f"  - {p}")

    if drift["modified_files"]:
        print("\n🟨 Modified files:")
        for p in drift["modified_files"]:
            print(f"  * {p}")

    if not any(drift.values()):
        print("✔️ No drift detected — structure is clean.")

    # Save drift output for TUI + CI
    with open(DRIFT_OUTPUT, "w") as f:
        json.dump(drift, f, indent=2)

    print(f"\n[+] Drift report saved to {DRIFT_OUTPUT}\n")


if __name__ == "__main__":
    main()
