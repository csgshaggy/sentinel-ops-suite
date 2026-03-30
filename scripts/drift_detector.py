#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "scripts" / "drift_snapshot.json"

IGNORE_DIRS = {
    "__pycache__",
    ".git",
    ".pytest_cache",
    "pytest_cache",
    "venv",
    "src/ssrf_command_console.egg-info",
}

IGNORE_EXT = {".pyc", ".pyo", ".pth"}

IGNORE_FILES = {str(SNAPSHOT.relative_to(ROOT))}


def should_ignore(path: Path) -> bool:
    rel = str(path.relative_to(ROOT))

    if rel in IGNORE_FILES:
        return True

    if any(part in IGNORE_DIRS for part in path.parts):
        return True

    if path.suffix in IGNORE_EXT:
        return True

    if "egg-info" in path.parts:
        return True

    return False


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_current_state():
    state = {}
    for p in ROOT.rglob("*"):
        if p.is_file() and not should_ignore(p):
            rel = str(p.relative_to(ROOT))
            state[rel] = hash_file(p)
    return state


def main() -> int:
    if not SNAPSHOT.exists():
        print("[!] No drift snapshot found. Run: make snapshot")
        return 1

    baseline = json.loads(SNAPSHOT.read_text())
    current = collect_current_state()

    added = sorted(set(current) - set(baseline))
    removed = sorted(set(baseline) - set(current))
    modified = sorted(
        [f for f in current if f in baseline and current[f] != baseline[f]]
    )

    if not (added or removed or modified):
        print("[*] No drift detected.")
        return 0

    print("[!] Drift detected:")
    if added:
        print("  [+] Added:")
        for f in added:
            print(f"      - {f}")

    if removed:
        print("  [-] Removed:")
        for f in removed:
            print(f"      - {f}")

    if modified:
        print("  [~] Modified:")
        for f in modified:
            print(f"      - {f}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
