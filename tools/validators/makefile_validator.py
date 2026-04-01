# tools/validators/makefile_validator.py

import sys
from pathlib import Path

REQUIRED_TARGETS = [
    "help",
    "venv",
    "install",
    "freeze",
    "lint",
    "lint-fix",
    "format",
    "backend-run",
    "backend-test",
    "frontend-install",
    "frontend-dev",
    "frontend-build",
    "pelm-run",
    "pelm-baseline",
    "pelm-diff",
    "anomaly-run",
    "anomaly-score",
    "idrim-run",
    "idrim-baseline",
    "idrim-diff",
    "ci-idrim-baseline",
    "validate-structure",
    "validate-makefile",
    "validate-all",
    "git-health",
    "git-repair",
    "snapshot-metadata",
    "clean",
    "clean-all",
]

def main() -> int:
    makefile = Path("Makefile")
    if not makefile.exists():
        print("Makefile not found", file=sys.stderr)
        return 1

    content = makefile.read_text()

    missing = []
    for target in REQUIRED_TARGETS:
        if f"\n{target}:" not in content and not content.startswith(f"{target}:"):
            missing.append(target)

    if missing:
        print("Missing required Makefile targets:", file=sys.stderr)
        for t in missing:
            print(f"  - {t}", file=sys.stderr)
        return 1

    print("Makefile validator: all required targets present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
