#!/usr/bin/env bash

source "$(dirname "$0")/banner.sh"

echo -e "[DOCTOR] Running environment diagnostics..."
echo ""

echo -e "[CHECK] Python version:"
python3 --version
echo ""

echo -e "[CHECK] Pip packages:"
pip list | head -20
echo ""

echo -e "[CHECK] Git branch:"
git rev-parse --abbrev-ref HEAD
echo ""

echo -e "[CHECK] Uncommitted changes:"
git status -s
echo ""

echo -e "[CHECK] Open ports (common dev ports):"
lsof -i :8000 -i :8080 -i :5000 -i :3000 2>/dev/null | sed 's/^/    /'
echo ""

echo -e "[DOCTOR] Done."
