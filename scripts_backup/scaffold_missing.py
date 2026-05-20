#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "scripts" / "repo_spec.json"


def main() -> int:
    if not SPEC.exists():
        print("[!] repo_spec.json missing")
        return 1

    spec = json.loads(SPEC.read_text())

    for d in spec.get("required_dirs", []):
        p = ROOT / d
        if not p.exists():
            print(f"[+] Creating directory: {d}")
            p.mkdir(parents=True, exist_ok=True)

    for f in spec.get("required_files", []):
        p = ROOT / f
        if not p.exists():
            print(f"[+] Creating file: {f}")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("")

    for f, content in spec.get("templates", {}).items():
        p = ROOT / f
        if not p.exists():
            print(f"[+] Creating template file: {f}")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)

    print("[*] Scaffolding complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
