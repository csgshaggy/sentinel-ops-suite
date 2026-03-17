#!/usr/bin/env bash
set -euo pipefail

# ----------------------------------------
# Color helpers
# ----------------------------------------
blue()  { printf "\033[34m%s\033[0m\n" "$1"; }
green() { printf "\033[32m%s\033[0m\n" "$1"; }
yellow(){ printf "\033[33m%s\033[0m\n" "$1"; }
red()   { printf "\033[31m%s\033[0m\n" "$1"; }

# ----------------------------------------
# Resolve script directory + project root
# ----------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$PROJECT_ROOT/docs"

if [[ ! -d "$DOCS_DIR" ]]; then
  red "ERROR: Could not find docs/ directory at: $DOCS_DIR"
  red "This script assumes the structure:"
  red "  project-root/"
  red "    docs/"
  red "    scripts/docs_organize.sh"
  exit 1
fi

blue "[0/3] Script directory: $SCRIPT_DIR"
blue "[0/3] Project root:     $PROJECT_ROOT"
blue "[0/3] Docs directory:    $DOCS_DIR"

# ----------------------------------------
# Create directory structure
# ----------------------------------------
blue "[1/3] Creating directory structure..."

dirs=(
  "00-index"
  "10-overview"
  "20-architecture"
  "30-configuration"
  "40-modes"
  "50-operations"
  "60-security"
  "70-development"
  "80-deployment"
  "90-governance"
  "95-examples"
  "99-meta"
)

for d in "${dirs[@]}"; do
  mkdir -p "$DOCS_DIR/$d"
done

green "Directory structure ready."

# ----------------------------------------
# Move helper
# ----------------------------------------
move() {
  local file="$1"
  local target="$2"

  if [[ -f "$DOCS_DIR/$file" ]]; then
    yellow "→ $file → $target/"
    mv "$DOCS_DIR/$file" "$DOCS_DIR/$target/"
  fi
}

# ----------------------------------------
# Move files into categories
# ----------------------------------------
blue "[2/3] Moving files into category directories..."

# 00-index
move "DOCS_INDEX.md"              "00-index"
move "README.md"                  "00-index"
move "GLOSSARY.md"                "00-index"
move "FAQ.md"                     "00-index"

# 10-overview
move "QUICKSTART.md"              "10-overview"
move "MANUAL.md"                  "10-overview"
move "FULL_LAB_GUIDE.md"          "10-overview"
move "TRAINING_LAB_SCENARIOS.md"  "10-overview"
move "OPERATOR_TRAINING.md"       "10-overview"

# 20-architecture
move "ARCHITECTURE_OVERVIEW.md"   "20-architecture"
move "DESIGN_DECISIONS.md"        "20-architecture"
move "API_VERSIONING_POLICY.md"   "20-architecture"

# 30-configuration
move "CONFIGURATION_REFERENCE.md" "30-configuration"
move "CONFIGURATION_EXAMPLES.md"  "30-configuration"
move "INSTALLATION_AND_SETUP.md"  "30-configuration"

# 40-modes
move "MODE_AUTHORING.md"          "40-modes"
move "MODE_CATALOG.md"            "40-modes"
move "MODE_EXAMPLES.md"           "40-modes"
move "MODE_TEMPLATES.md"          "40-modes"
move "MODE_IDEAS_CATALOG.md"      "40-modes"
move "ADVANCED_MODE_PATTERNS.md"  "40-modes"

# 50-operations
move "OPERATOR_GUIDE.md"          "50-operations"
move "SERVICE_DEPLOYMENT.md"      "50-operations"
move "SERVICE_HARDENING.md"       "50-operations"
move "DEPLOYMENT_CHECKLIST.md"    "50-operations"
move "OBSERVABILITY_GUIDE.md"     "50-operations"
move "PERFORMANCE_GUIDE.md"       "50-operations"
move "BENCHMARK_RESULTS.md"       "50-operations"

# 60-security
move "SECURITY_MODEL.md"          "60-security"
move "SECURITY_RESPONSE_PROCESS.md" "60-security"
move "KNOWN_LIMITATIONS.md"       "60-security"
move "ADVANCED_SSRF_TECHNIQUES.md" "60-security"

# 70-development
move "DEVELOPER_GUIDE.md"         "70-development"
move "API_REFERENCE.md"           "70-development"
move "API_CONTRACTS.md"           "70-development"
move "CONTRIBUTING.md"            "70-development"
move "CONTRIBUTOR_TROUBLESHOOTING.md" "70-development"
move "EXTENSION_SDK.md"           "70-development"

# 80-deployment
move "RELEASE_PROCESS.md"         "80-deployment"
move "UPGRADE_GUIDE.md"           "80-deployment"
move "ROADMAP.md"                 "80-deployment"

# 90-governance
move "CHANGELOG.md"               "90-governance"

# 95-examples
move "REAL_WORLD_EXAMPLES.md"     "95-examples"

# 99-meta
move "STYLE_GUIDE.md"             "99-meta"

# testing
move "TESTING_GUIDE.md"           "testing"

green "[3/3] All files moved successfully."
blue "Done."
