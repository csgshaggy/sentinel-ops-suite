#!/usr/bin/env python3
"""
Drift Dashboard Generator
Generates a Markdown drift dashboard for GitHub Pages.
"""

import sys
from pathlib import Path
import json

# ---------------------------------------------------------
# Ensure the scripts/ directory is importable
# ---------------------------------------------------------
# This file lives in: scripts/ci/drift_dashboard.py
# drift_detector.py lives in: scripts/drift_detector.py
# So we add the parent directory of this file (scripts/) to PYTHONPATH.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from drift_detector import walk_tree, load_baseline, compare  # noqa: E402

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = REPO_ROOT / "runtime" / "baseline.json"
OUTPUT_DIR = REPO_ROOT / "runtime"
OUTPUT_MD = OUTPUT_DIR / "drift_dashboard.md"
OUTPUT_JSON = OUTPUT_DIR / "drift_results.json"


# ---------------------------------------------------------
# Dashboard Generation
# ---------------------------------------------------------
def generate_dashboard():
    print("[INFO] Loading baseline...")
    baseline = load_baseline(BASELINE_PATH)

    print("[INFO] Walking repository tree...")
    current = walk_tree(REPO_ROOT)

    print("[INFO] Comparing baseline to current state...")
    results = compare(baseline, current)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Writing JSON results → {OUTPUT_JSON}")
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)

    print(f"[INFO] Writing Markdown dashboard → {OUTPUT_MD}")
    with open(OUTPUT_MD, "w") as f:
        f.write("# Drift Dashboard\n\n")
        f.write("## Summary\n")
        f.write(f"- Added: {len(results['added'])}\n")
        f.write(f"- Removed: {len(results['removed'])}\n")
        f.write(f"- Modified: {len(results['modified'])}\n\n")

        f.write("## Added Files\n")
        for item in results["added"]:
            f.write(f"- `{item}`\n")
        f.write("\n")

        f.write("## Removed Files\n")
        for item in results["removed"]:
            f.write(f"- `{item}`\n")
        f.write("\n")

        f.write("## Modified Files\n")
        for item in results["modified"]:
            f.write(f"- `{item}`\n")
        f.write("\n")

    print("[OK] Drift dashboard generated successfully.")


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    generate_dashboard()
