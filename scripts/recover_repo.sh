#!/usr/bin/env bash
set -euo pipefail

echo "[*] In-place repository recovery (hard reset to origin/main)"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[!] Not inside a git repository. Run this from the repo root."
  exit 1
fi

echo "[*] Fetching from origin..."
git fetch origin

echo "[*] Resetting to origin/main..."
git reset --hard origin/main

echo "[*] Cleaning untracked files..."
git clean -fdx

echo "[*] Verifying repo integrity..."
git fsck --full

echo "[*] Running automated layout + health validation..."
if [ -x scripts/validate_repo.py ]; then
  python3 scripts/validate_repo.py || true
else
  echo "    (no scripts/validate_repo.py yet; create it to enforce structure/health)"
fi

echo "[*] Recovery complete at: $(pwd)"
