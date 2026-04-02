#!/bin/bash

echo "=========================================="
echo "        Makefile Baseline Diff Viewer"
echo "=========================================="

if [ ! -f .meta/makefile/Makefile.baseline ]; then
    echo "❌ No baseline found."
    exit 1
fi

diff -u .meta/makefile/Makefile.baseline Makefile || true

echo
read -p "Press Enter to return..."
