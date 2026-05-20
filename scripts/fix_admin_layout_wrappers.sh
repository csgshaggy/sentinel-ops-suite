#!/bin/bash
set -e

ROOT="/home/ubuntu/sentinel-ops-suite/frontend/unified-frontend"
ADMIN_DIR="$ROOT/src/pages/admin"

echo "== Removing nested Layout wrappers from admin pages =="

for FILE in "$ADMIN_DIR"/*.jsx; do
    echo "[*] Processing: $(basename "$FILE")"

    # 1. Remove the Layout import
    sed -i '/import Layout/d' "$FILE"

    # 2. Remove opening <Layout ...> tag
    sed -i 's/<Layout[^>]*>//g' "$FILE"

    # 3. Remove closing </Layout> tag
    sed -i 's/<\/Layout>//g' "$FILE"
done

echo "== Admin Layout cleanup complete =="
echo "== Rebuilding project =="

cd "$ROOT"
npm run build

echo "== Reloading nginx =="
sudo nginx -t && sudo systemctl reload nginx

echo "== DONE. Admin pages no longer render nested Layouts. =="
