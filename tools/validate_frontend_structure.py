import os
import sys
from pathlib import Path

ROOT = Path("frontend/src")

REQUIRED_DIRS = [
    ROOT / "pages",
    ROOT / "components",
]

REQUIRED_FILES = [
    ROOT / "pages/PelmConsole.tsx",
    ROOT / "components/PelmRiskTrend.tsx",
    ROOT / "components/PelmSnapshotDiff.tsx",
    ROOT / "components/PelmRegressionPanel.tsx",
    ROOT / "components/PelmAlerts.tsx",
    ROOT / "components/SeverityBadge.tsx",
]

ALLOWED_COMPONENTS = {
    "PelmRiskTrend.tsx",
    "PelmSnapshotDiff.tsx",
    "PelmRegressionPanel.tsx",
    "PelmAlerts.tsx",
    "SeverityBadge.tsx",
}

def fail(msg):
    print(f"[STRUCTURE ERROR] {msg}")
    sys.exit(1)

def main():
    # Check required directories
    for d in REQUIRED_DIRS:
        if not d.exists():
            fail(f"Missing directory: {d}")

    # Check required files
    for f in REQUIRED_FILES:
        if not f.exists():
            fail(f"Missing file: {f}")

    # Check for unexpected files in components/
    comp_dir = ROOT / "components"
    for f in comp_dir.iterdir():
        if f.is_file() and f.name not in ALLOWED_COMPONENTS:
            fail(f"Unexpected file in components/: {f.name}")

    print("[OK] Frontend structure is valid and drift‑free.")

if __name__ == "__main__":
    main()
