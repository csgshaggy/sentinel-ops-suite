#!/usr/bin/env bash

source "$(dirname "$0")/banner.sh"

echo -e "[TREE] Project structure:"
echo ""

tree -I "__pycache__|.pytest_cache|.mypy_cache|.git|dist|build"
