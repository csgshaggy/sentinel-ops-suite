#!/usr/bin/env bash
set -euo pipefail

BLUE="\033[94m"
GREEN="\033[92m"
YELLOW="\033[93m"
RED="\033[91m"
END="\033[0m"

info()  { echo -e "${BLUE}[INFO]${END} $1"; }
ok()    { echo -e "${GREEN}[OK]${END} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${END} $1"; }
fail()  { echo -e "${RED}[FAIL]${END} $1"; exit 1; }

# ---------------------------------------------------------
# Required directories
# ---------------------------------------------------------
info "Checking required directories..."

REQUIRED_DIRS=(
  "scripts"
  "scripts/ci"
  "scripts/doctor"
  "runtime"
  "docs"
  ".github/workflows"
  ".github/scripts"
)

for d in "${REQUIRED_DIRS[@]}"; do
  if [[ ! -d "$d" ]]; then
    fail "Missing directory: $d"
  else
    ok "Found: $d"
  fi
done

# ---------------------------------------------------------
# Required files
# ---------------------------------------------------------
info "Checking required files..."

REQUIRED_FILES=(
  "scripts/drift_detector.py"
  "scripts/ci/drift_dashboard.py"
  "scripts/ci/doctor_dashboard.py"
  "scripts/doctor/run_doctor.py"
  "Makefile"
)

for f in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    fail "Missing file: $f"
  else
    ok "Found: $f"
  fi
done

# ---------------------------------------------------------
# Makefile target validation
# ---------------------------------------------------------
info "Checking Makefile targets..."

TARGETS=(
  "doctor"
  "baseline"
  "drift"
  "drift-dashboard"
  "ci-drift"
  "ci-doctor"
  "clean-runtime"
)

for t in "${TARGETS[@]}"; do
  if ! grep -qE "^$t:" Makefile; then
    fail "Missing Makefile target: $t"
  else
    ok "Target exists: $t"
  fi
done

# ---------------------------------------------------------
# Runtime hygiene
# ---------------------------------------------------------
info "Checking runtime directory hygiene..."

mkdir -p runtime

BAD_FILES=$(find runtime -maxdepth 1 -type f ! -name "*.json" ! -name "*.md" | wc -l)

if [[ "$BAD_FILES" -gt 0 ]]; then
  warn "Unexpected files found in runtime/:"
  find runtime -maxdepth 1 -type f ! -name "*.json" ! -name "*.md"
  fail "Runtime directory contains non‑operational files."
else
  ok "Runtime directory clean."
fi

ok "Repo integrity checks passed."
