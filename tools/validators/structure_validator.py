# tools/validators/structure_validator.py

import sys
from pathlib import Path

# Minimal, operator-grade structure expectations.
REQUIRED_PATHS = [
    # Core
    "Makefile",
    "requirements.txt",

    # Backend
    "backend/app/main.py",
    "backend/app/routers",

    # Frontend
    "frontend/package.json",
    "frontend/tsconfig.json",

    # Tools / Validators
    "tools/validators/makefile_validator.py",
    "tools/validators/structure_validator.py",

    # Security / IDRIM
    "tools/security/idrim/idrim_engine.py",
    "tools/security/idrim/collectors/iam_collector.py",
    "tools/security/idrim/collectors/role_collector.py",
    "tools/security/idrim/collectors/group_collector.py",
    "tools/security/idrim/baselines/baseline_manager.py",
    "tools/security/idrim/analyzers/drift_analyzer.py",
    "tools/security/idrim/analyzers/privilege_delta.py",
    "tools/security/idrim/outputs/idrim_event.py",
    "tools/security/idrim/outputs/idrim_reporter.py",

    # Routers / Dashboard
    "backend/app/routers/idrim_router.py",
    "frontend/dashboard/panels/IDRIMPanel.tsx",
]


def main() -> int:
    missing = []

    for rel in REQUIRED_PATHS:
        p = Path(rel)
        if not p.exists():
            missing.append(rel)

    if missing:
        print("Structure validator: missing required paths:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    print("Structure validator: all required paths present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
