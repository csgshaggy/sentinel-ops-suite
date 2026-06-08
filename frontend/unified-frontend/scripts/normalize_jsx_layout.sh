#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[2] Normalizing JSX layout wrappers under: $ROOT_DIR/src"

# 1. Legacy container wrappers → page-container
find "$ROOT_DIR/src" -name "*.jsx" -print0 | xargs -0 sed -i \
  -e 's/className="container"/className="page-container"/g' \
  -e 's/className="content-wrapper"/className="page-container"/g' \
  -e 's/className={"container"}/className="page-container"/g'

# 2. Panels → glass
find "$ROOT_DIR/src" -name "*.jsx" -print0 | xargs -0 sed -i \
  -e 's/className="card"/className="glass"/g' \
  -e 's/className="panel"/className="glass"/g'

# 3. Combined wrappers (if any)
find "$ROOT_DIR/src" -name "*.jsx" -print0 | xargs -0 sed -i \
  -e 's/className="container glass"/className="page-container glass"/g' \
  -e 's/className="content-wrapper glass"/className="page-container glass"/g'

echo "[2] JSX layout normalization complete."
