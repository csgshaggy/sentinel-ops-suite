#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[3] Normalizing glow, neon, and accent usage under: $ROOT_DIR/src"

# 1. Text shadows → theme glow
find "$ROOT_DIR/src" -name "*.css" -print0 | xargs -0 sed -i \
  -e 's/text-shadow:\s*0 0 10px #00eaff;/text-shadow: var(--glow-cyan);/g' \
  -e 's/text-shadow:\s*0 0 10px rgba(0,\s*234,\s*255,\s*0\.7);/text-shadow: var(--glow-cyan);/g'

# 2. Neon accent color → theme accent
find "$ROOT_DIR/src" -name "*.css" -print0 | xargs -0 sed -i \
  -e 's/#00eaff/var(--accent)/g' \
  -e 's/rgba(0,\s*234,\s*255,\s*0\.25)/var(--neon-accent-soft)/g'

# 3. Button backgrounds → theme
find "$ROOT_DIR/src" -name "*.css" -print0 | xargs -0 sed -i \
  -e 's/background:\s*#00eaff;/background: var(--btn-primary-bg);/g' \
  -e 's/background:\s*#00c8ff;/background: var(--btn-primary-bg);/g'

echo "[3] Glow and accent normalization complete."
