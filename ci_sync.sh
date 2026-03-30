#!/usr/bin/env bash
set -euo pipefail

echo "=== CI Sync Mirror ==="

# Auto-repair permissions
./auto_repair_permissions.sh

# Validate structure
make validate-structure

# Drift detection
make drift

# Lint + format checks
make lint
make format

# CI gates
make self-check
make ci-fast

# Build frontend
cd frontend
npm install
npm run build
cd ..

# Build backend
cd backend
pip install -r requirements.txt
python -m py_compile $(find app -name "*.py")
cd ..

echo "=== CI Sync Mirror Complete ==="
