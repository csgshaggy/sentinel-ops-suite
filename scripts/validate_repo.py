#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "scripts" / "repo_spec.json"


def main() -> int:
    if not SPEC_PATH.exists():
        print(f"[!] Spec file missing: {SPEC_PATH}")
        return 1

    try:
        spec = json.loads(SPEC_PATH.read_text())
    except Exception as e:
        print(f"[!] Failed to parse repo_spec.json: {e}")
        return 1

    missing = []

    for d in spec.get("required_dirs", []):
        if not (ROOT / d).is_dir():
            missing.append(f"DIR  {d}")

    for f in spec.get("required_files", []):
        if not (ROOT / f).is_file():
            missing.append(f"FILE {f}")

    if missing:
        print("[!] Repository is missing required items:")
        for m in missing:
            print(f"    - {m}")
        return 1

    print("[*] Repository structure matches spec.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
