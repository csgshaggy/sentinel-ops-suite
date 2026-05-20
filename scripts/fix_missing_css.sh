#!/bin/bash
set -e

ROOT="/home/ubuntu/sentinel-ops-suite/frontend/unified-frontend"

echo "== Fixing Missing CSS Imports =="

# Remove broken imports
echo "[1] Removing broken CSS imports..."
sed -i '/ErrorPages.css/d' "$ROOT/src/pages/ServerError.jsx"
sed -i '/ErrorPages.css/d' "$ROOT/src/pages/NotFound.jsx"
sed -i '/brand.css/d' "$ROOT/src/pages/NotFound.jsx"
sed -i '/AuthLayout.css/d' "$ROOT/src/layouts/AuthLayout.jsx"
sed -i '/modal.css/d' "$ROOT/src/App.jsx"
sed -i '/panels.css/d' "$ROOT/src/components/Panel.jsx"

# Recreate minimal CSS directories
echo "[2] Recreating minimal CSS directories..."
mkdir -p "$ROOT/src/styles/errors"
mkdir -p "$ROOT/src/styles/auth"
mkdir -p "$ROOT/src/styles"

# Create placeholder CSS files
echo "[3] Writing placeholder CSS files..."

cat > "$ROOT/src/styles/errors/ErrorPages.css" << 'EOF'
/* Placeholder error page styles */
.error-page {
  padding: 40px;
  text-align: center;
  color: var(--text-primary);
}
EOF

cat > "$ROOT/src/styles/auth/brand.css" << 'EOF'
/* Placeholder brand styles */
.auth-brand {
  text-align: center;
  margin-bottom: 20px;
}
EOF

cat > "$ROOT/src/styles/auth/AuthLayout.css" << 'EOF'
/* Placeholder auth layout styles */
.auth-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
}
EOF

cat > "$ROOT/src/styles/modal.css" << 'EOF'
/* Placeholder modal styles */
.modal {
  background: var(--bg-surface);
  padding: 20px;
  border-radius: 8px;
}
EOF

cat > "$ROOT/src/styles/panels.css" << 'EOF'
/* Placeholder panel styles */
.panel {
  background: var(--bg-surface);
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}
EOF

echo "[4] Rebuilding..."
cd "$ROOT"
npm run build

echo "[5] Reloading nginx..."
sudo nginx -t && sudo systemctl reload nginx

echo "== Missing CSS Fix Complete =="
