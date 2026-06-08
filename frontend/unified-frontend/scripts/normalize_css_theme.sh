#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[1] Normalizing CSS theme usage under: $ROOT_DIR/src"

# 1. Raw glass backgrounds → theme glass
find "$ROOT_DIR/src" -name "*.css" -print0 | xargs -0 sed -i \
  -e 's/background:\s*rgba(255,\s*255,\s*255,\s*0\.05);/background: var(--glass-bg);/g' \
  -e 's/background:\s*rgba(255,\s*255,\s*255,\s*0\.06);/background: var(--glass-bg);/g' \
  -e 's/background:\s*rgba(255,\s*255,\s*255,\s*0\.12);/background: var(--glass-bg-strong);/g'

# 2. Raw dark panel backgrounds → theme panel
find "$ROOT_DIR/src" -name "*.css" -print0 | xargs -0 sed -i \
  -e 's/background:\s*#14171c;/background: var(--background-panel);/g' \
  -e 's/background:\s*#0d0f12;/background: var(--bg-root);/g'

# 3. Radius normalization
find "$ROOT_DIR/src" -name "*.css" -print0 | xargs -0 sed -i \
  -e 's/border-radius:\s*10px;/border-radius: var(--radius);/g' \
  -e 's/border-radius:\s*12px;/border-radius: var(--radius);/g' \
  -e 's/border-radius:\s*8px;/border-radius: var(--radius-sm);/g'

# 4. Text colors → theme
find "$ROOT_DIR/src" -name "*.css" -print0 | xargs -0 sed -i \
  -e 's/color:\s*#ffffff;/color: var(--text-primary);/g' \
  -e 's/color:\s*#9ca3af;/color: var(--text-secondary);/g'

# 5. Borders → glass border
find "$ROOT_DIR/src" -name "*.css" -print0 | xargs -0 sed -i \
  -e 's/border-bottom:\s*1px solid #222;/border-bottom: 1px solid var(--glass-border);/g' \
  -e 's/border:\s*1px solid #333;/border: 1px solid var(--glass-border);/g'

echo "[1] CSS theme normalization complete."
