#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

RED="$(printf '\033[31m')"
GREEN="$(printf '\033[32m')"
YELLOW="$(printf '\033[33m')"
BLUE="$(printf '\033[34m')"
BOLD="$(printf '\033[1m')"
RESET="$(printf '\033[0m')"

info()  { printf "%s[INFO]%s %s\n"  "$BLUE"  "$RESET" "$*"; }
warn()  { printf "%s[WARN]%s %s\n"  "$YELLOW""$RESET" "$*"; }
ok()    { printf "%s[ OK ]%s %s\n"  "$GREEN""$RESET" "$*"; }
err()   { printf "%s[FAIL]%s %s\n"  "$RED"  "$RESET" "$*"; }

if [[ ! -d "$PROJECT_ROOT" ]]; then
  err "PROJECT_ROOT does not exist: $PROJECT_ROOT"
  exit 1
fi

info "Using PROJECT_ROOT: $PROJECT_ROOT"

cd "$PROJECT_ROOT"

# 1) Remove Python cache and build artifacts
info "Removing Python cache and build artifacts..."
find . -type d -name "__pycache__" -prune -exec rm -rf {} + || true
find . -type f -name "*.pyc" -delete || true
find . -type f -name "*.pyo" -delete || true
rm -rf \
  .pytest_cache \
  .mypy_cache \
  .ruff_cache \
  build \
  dist \
  *.egg-info \
  .coverage \
  coverage.xml \
  htmlcov 2>/dev/null || true
ok "Python cache and build artifacts removed."

# 2) Remove common editor/OS junk
info "Removing editor and OS junk files..."
find . -type f \( \
  -name "*~" -o \
  -name ".*.swp" -o \
  -name ".*.swo" -o \
  -name ".DS_Store" -o \
  -name "Thumbs.db" \
\) -delete || true
ok "Editor/OS junk removed."

# 3) Remove stray scan/output debris (customize as needed)
info "Removing known scan/output debris..."
rm -rf \
  tmp \
  temp \
  logs/tmp \
  scratch \
  .scanner-output \
  .scan-results \
  .tmp-output 2>/dev/null || true
ok "Scan/output debris removed (where present)."

# 4) Optional: clean old log archives (keep current logs)
LOG_DIR="$PROJECT_ROOT/logs"
if [[ -d "$LOG_DIR" ]]; then
  info "Cleaning old log archives in: $LOG_DIR"
  find "$LOG_DIR" -type f \( -name "*.log.old" -o -name "*.log.*.gz" \) -delete || true
  ok "Old log archives cleaned."
else
  warn "No logs directory found at $LOG_DIR (skipping log cleanup)."
fi

ok "Cleanup completed successfully."
