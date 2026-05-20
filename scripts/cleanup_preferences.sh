#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"

echo "=== Sentinel Ops Suite — Preferences Cleanup (Safe Version) ==="
echo "Project root: $ROOT"
echo

# ---------------------------------------------------------
# TARGETS
# ---------------------------------------------------------
TARGET_FILES=(
  "src/pages/PreferencesPage.jsx"
  "src/context/ThemeManager.jsx"
)

TARGET_PATTERNS=(
  "PreferencesPage"
  "ThemeManager"
  "/preferences"
  "preferences"
)

TARGET_DIRS=(
  "src/components/preferences"
)

# ---------------------------------------------------------
# DRY RUN MODE
# ---------------------------------------------------------
if [[ "${1:-}" == "--dry-run" ]]; then
  echo "[DRY RUN] Listing files that would be removed:"
  echo

  for f in "${TARGET_FILES[@]}"; do
    [[ -f "$f" ]] && echo "  FILE: $f"
  done

  for d in "${TARGET_DIRS[@]}"; do
    [[ -d "$d" ]] && echo "  DIR:  $d"
  done

  echo
  echo "[DRY RUN] Listing files that would be patched:"
  echo

  for pattern in "${TARGET_PATTERNS[@]}"; do
    grep -RIl "$pattern" src || true
  done

  echo
  echo "Dry run complete."
  exit 0
fi

# ---------------------------------------------------------
# DELETE TARGET FILES
# ---------------------------------------------------------
echo "Removing legacy files..."
for f in "${TARGET_FILES[@]}"; do
  if [[ -f "$f" ]]; then
    echo "  DELETE: $f"
    rm -f "$f"
  fi
done

# ---------------------------------------------------------
# DELETE TARGET DIRECTORIES
# ---------------------------------------------------------
echo "Removing legacy directories..."
for d in "${TARGET_DIRS[@]}"; do
  if [[ -d "$d" ]]; then
    echo "  DELETE DIR: $d"
    rm -rf "$d"
  fi
done

# ---------------------------------------------------------
# PATCH IMPORTS & ROUTES (slash‑safe sed)
# ---------------------------------------------------------
echo "Patching imports and routes..."

for pattern in "${TARGET_PATTERNS[@]}"; do
  # Escape slashes for sed
  safe_pattern=$(printf '%s\n' "$pattern" | sed 's/[\/&]/\\&/g')

  grep -RIl "$pattern" src | while read -r file; do
    echo "  PATCH: $file (remove '$pattern')"
    sed -i.bak "/$safe_pattern/d" "$file"
  done
done

# ---------------------------------------------------------
# CLEANUP .bak FILES
# ---------------------------------------------------------
echo "Cleaning up backup files..."
find src -type f -name "*.bak" -delete

echo
echo "=== Cleanup complete (Safe Version) ==="
echo "Preferences system fully removed."
