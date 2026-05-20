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

cd "$PROJECT_ROOT"
info "Auto-repairing project structure at: $PROJECT_ROOT"

# ------------------------------------------------------------
# Ensure core directories
# ------------------------------------------------------------
ensure_dir() {
  local path="$1"
  if [[ -d "$path" ]]; then
    ok "Directory exists: $path"
  else
    warn "Missing directory: $path (creating)"
    mkdir -p "$path"
    ok "Created directory: $path"
  fi
}

ensure_dir "src"
ensure_dir "src/ssrf_command_console"
ensure_dir "scripts"
ensure_dir "tests"
ensure_dir "logs"
ensure_dir ".internal"

# ------------------------------------------------------------
# Ensure core files
# ------------------------------------------------------------
ensure_file() {
  local path="$1"
  local template="$2"

  if [[ -f "$path" ]]; then
    ok "File exists: $path"
  else
    warn "Missing file: $path (creating)"
    printf "%s\n" "$template" > "$path"
    ok "Created file: $path"
  fi
}

# Minimal pyproject.toml if missing
PYPROJECT_TEMPLATE='[project]
name = "ssrf-command-console"
version = "0.1.0"
description = "SSRF Command Console"
requires-python = ">=3.10"

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
'

ensure_file "pyproject.toml" "$PYPROJECT_TEMPLATE"
ensure_file "README.md" "# ssrf-command-console"
ensure_file "LICENSE" "TODO: Add license text"

# ------------------------------------------------------------
# Ensure package init and basic modules
# ------------------------------------------------------------
ensure_file "src/ssrf_command_console/__init__.py" "from .version import __version__"
ensure_file "src/ssrf_command_console/version.py" '__version__ = "0.1.0"'
ensure_file "src/ssrf_command_console/core/__init__.py" ""
ensure_dir  "src/ssrf_command_console/core"

ensure_file "src/ssrf_command_console/core/engine.py" \
'def hello():
    return "ssrf_command_console core engine active"
'

# ------------------------------------------------------------
# Ensure basic tests
# ------------------------------------------------------------
ensure_file "tests/test_core.py" \
'from ssrf_command_console.core.engine import hello

def test_hello():
    assert hello() == "ssrf_command_console core engine active"
'

# ------------------------------------------------------------
# Final message
# ------------------------------------------------------------
ok "Auto-repair completed. You can now run ./scripts/validate_project_tree.sh"
