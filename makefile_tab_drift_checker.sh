#!/usr/bin/env bash
set -euo pipefail

FILE="Makefile"

if [[ ! -f "$FILE" ]]; then
  echo "Makefile not found" >&2
  exit 1
fi

echo "🔍 Checking Makefile for tab drift..."

# 1) Any command lines starting with spaces (likely drift)
violations=$(python3 - << 'EOF'
from pathlib import Path
import sys

mf = Path("Makefile")
bad = []
with mf.open("r", encoding="utf-8") as f:
    prev = ""
    for idx, line in enumerate(f, start=1):
        if line.strip() and not line.lstrip().startswith("#"):
            candidate_prev = line.rstrip("\n")
        else:
            candidate_prev = prev

        if line.startswith(" ") and prev.strip().endswith(":"):
            bad.append((idx, line.rstrip("\n")))

        if line.strip() and not line.lstrip().startswith("#"):
            prev = candidate_prev

if bad:
    for ln, content in bad:
        print(f"{ln}:{content}")
    sys.exit(1)
EOF
) || {
  echo "❌ Tab drift detected in Makefile (spaces where TAB commands expected):"
  echo "$violations"
  exit 1
}

echo "✔ No tab drift detected in Makefile."
