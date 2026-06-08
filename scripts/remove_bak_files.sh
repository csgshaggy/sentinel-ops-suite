#!/bin/bash
set -euo pipefail

echo "[SCAN] Finding .bak files under src/..."
find src -type f -name "*.bak"

echo
echo "[DELETE] Removing .bak files from src/..."
find src -type f -name "*.bak" -exec rm -f {} \;

echo
echo "[VERIFY] Ensuring no .bak files remain..."
find src -type f -name "*.bak" || echo "[OK] No .bak files remain."

echo
echo "[DONE] All .bak files removed. Rebuild required."
