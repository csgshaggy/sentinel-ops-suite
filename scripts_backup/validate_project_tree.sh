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
warn()  { printf "%s[WARN]%s %s\n"  "$YELLOW" "$RESET" "$*"; }
ok()    { printf "%s[ OK ]%s %s\n"  "$GREEN" "$RESET" "$*"; }
err()   { printf "%s[FAIL]%s %s\n" "$RED" "$RESET" "$*"; }

if [[ ! -d "$PROJECT_ROOT" ]]; then
  err "PROJECT_ROOT does not exist: $PROJECT_ROOT"
  exit 1
fi

cd "$PROJECT_ROOT"
info "Validating project tree at: $PROJECT_ROOT"

STATUS=0

check_dir() {
  local path="$1"
  if [[ -d "$path" ]]; then
    ok "Directory exists: $path"
  else
    warn "Missing directory: $path"
    STATUS=1
  fi
}

check_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    ok "File exists: $path"
  else
    warn "Missing file: $path"
    STATUS=1
  fi
}

###############################################
# 1) Core directories
###############################################
info "Checking core directories..."
check_dir "src"
check_dir "src/ssrf_command_console"
check_dir "scripts"
check_dir "tests"

###############################################
# 2) Core files
###############################################
info "Checking core files..."
check_file "pyproject.toml"
check_file "README.md"
check_file "LICENSE"

###############################################
# 3) Legacy name scan
###############################################
info "Scanning for legacy name 'ssrf-console'..."
if rg -n "ssrf-console" . 2>/dev/null; then
  err "Found legacy 'ssrf-console' references above. Please fix."
  STATUS=1
else
  ok "No legacy 'ssrf-console' references found."
fi

###############################################
# 4) Package usage check
###############################################
info "Checking for 'ssrf_command_console' usage..."
if rg -n "ssrf_command_console" src tests 2>/dev/null; then
  ok "Found 'ssrf_command_console' references in code."
else
  warn "No 'ssrf_command_console' references found in src/tests. Verify package usage."
fi

###############################################
# 5) Suspicious top-level clutter
###############################################
info "Checking for suspicious top-level clutter..."

# Allowed top-level files
ALLOWED=(
  "pyproject.toml"
  "README.md"
  "LICENSE"
  ".gitignore"
  "*.md"
  ".env*"
  "run.py"
  "requirements.in"
  "requirements.txt"
  "requirements.lock"
  "Makefile"
  "ci_test.txt"
)

# Build exclusion flags
EXCLUDES=()
for a in "${ALLOWED[@]}"; do
  EXCLUDES+=(! -name "$a")
done

# Find suspicious files
SUSPECTS=$(find . -maxdepth 1 -type f \
  ! -name "pyproject.toml" \
  ! -name "README.md" \
  ! -name "LICENSE" \
  ! -name ".gitignore" \
  ! -name "*.md" \
  ! -name ".env*" \
  ! -name "run.py" \
  ! -name "requirements.in" \
  ! -name "requirements.txt" \
  ! -name "requirements.lock" \
  ! -name "Makefile" \
  ! -name "ci_test.txt" \
  | sed 's|^\./||' || true)

if [[ -n "${SUSPECTS:-}" ]]; then
  warn "Suspicious top-level files (review manually):"
  printf "  - %s\n" $SUSPECTS
  STATUS=1
else
  ok "No suspicious top-level files detected."
fi

###############################################
# Final status
###############################################
if [[ "$STATUS" -eq 0 ]]; then
  ok "Project tree validation PASSED."
else
  err "Project tree validation completed with issues."
fi

exit "$STATUS"
