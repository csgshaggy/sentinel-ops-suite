# tools/validators/repo_drift_detector.py

import sys
from pathlib import Path
import hashlib
import json

ROOT = Path(".")
CANONICAL_PATH = Path("tools/validators/canonical_repo_manifest.json")


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def build_manifest(root: Path) -> dict:
    manifest: dict[str, str] = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        # Skip canonical files themselves
        if str(p).startswith("tools/validators/canonical_"):
            continue
        manifest[str(p)] = file_hash(p)
    return manifest


def main() -> int:
    if not CANONICAL_PATH.exists():
        print(f"Canonical repo manifest not found: {CANONICAL_PATH}", file=sys.stderr)
        return 1

    current = build_manifest(ROOT)
    canonical = json.loads(CANONICAL_PATH.read_text())

    added = sorted(set(current) - set(canonical))
    removed = sorted(set(canonical) - set(current))
    changed = sorted(
        p for p in current.keys() & canonical.keys()
        if current[p] != canonical[p]
    )

    if not (added or removed or changed):
        print("Repo drift detector: no drift detected.")
        return 0

    print("Repo drift detected:")
    if added:
        print("  Added files:")
        for p in added:
            print(f"    + {p}")
    if removed:
        print("  Removed files:")
        for p in removed:
            print(f"    - {p}")
    if changed:
        print("  Modified files:")
        for p in changed:
            print(f"    * {p}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
