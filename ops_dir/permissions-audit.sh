#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY="${DRY_RUN:-0}"

echo "🔐 Sentinel Ops — Permissions Audit"
echo "📁 Repo: $REPO_ROOT"
echo "🧪 DRY RUN: $DRY"
echo

# ----------------------------------------
# Color helpers
# ----------------------------------------
ok()    { echo -e "  \e[32m✔\e[0m $1"; }
warn()  { echo -e "  \e[33m⚠\e[0m $1"; }
fix()   { echo -e "  \e[36m🔧\e[0m $1"; }
err()   { echo -e "  \e[31m✘\e[0m $1"; }

# ----------------------------------------
# File patterns that MUST be executable
# ----------------------------------------
TARGETS=(
  "ops"
  "ops_dir/*.sh"
  "scripts/**/*.sh"
  "scripts/**/*.mjs"
)

# ----------------------------------------
# Expand globs safely
# ----------------------------------------
expand_glob() {
  shopt -s globstar nullglob
  echo $1
  shopt -u globstar nullglob
}

# ----------------------------------------
# Audit loop
# ----------------------------------------
missing=0

for pattern in "${TARGETS[@]}"; do
  for file in $(expand_glob "$REPO_ROOT/$pattern"); do
    if [[ -f "$file" ]]; then
      if [[ ! -x "$file" ]]; then
        warn "Missing +x: ${file#$REPO_ROOT/}"
        ((missing++))

        if [[ "$DRY" -eq 0 ]]; then
          chmod +x "$file"
          fix "Applied +x to ${file#$REPO_ROOT/}"
        else
          fix "Would apply +x to ${file#$REPO_ROOT/}"
        fi
      else
        ok "Executable: ${file#$REPO_ROOT/}"
      fi
    fi
  done
done

echo
if [[ "$missing" -eq 0 ]]; then
  ok "All required files already have +x permissions."
else
  if [[ "$DRY" -eq 1 ]]; then
    warn "$missing file(s) missing +x — DRY RUN mode, no changes applied."
  else
    ok "Fixed $missing file(s) missing +x."
  fi
fi

echo "🔐 Permissions audit complete."
