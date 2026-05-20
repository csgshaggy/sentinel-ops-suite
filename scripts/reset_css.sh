#!/bin/bash
set -e

ROOT="/home/ubuntu/sentinel-ops-suite/frontend/unified-frontend"
STYLES="$ROOT/src/styles"
COMPONENTS="$ROOT/src/components"

echo "== Sentinel Ops CSS Reset =="

echo "[1] Backing up existing styles directory..."
if [ -d "$STYLES" ]; then
    mv "$STYLES" "${STYLES}_backup_$(date +%s)"
fi

echo "[2] Recreating clean styles directory..."
mkdir -p "$STYLES"

echo "[3] Writing clean global.css..."
cat > "$STYLES/global.css" << 'EOF'
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #root {
  height: 100%;
  width: 100%;
  overflow: hidden;
  background: var(--bg-root);
  color: var(--text-primary);
  font-family: "Inter", sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font-family: inherit;
}
EOF

echo "[4] Writing clean theme.css placeholder..."
cat > "$STYLES/theme.css" << 'EOF'
:root {
  --bg-root: #0d0f12;
  --bg-surface: #14171c;
  --text-primary: #ffffff;
  --text-secondary: #9ca3af;
  --neon-accent: #00eaff;
  --neon-accent-soft: rgba(0, 234, 255, 0.25);
  --glass-blur: blur(12px);
}
EOF

echo "[5] Writing clean session-expire.css placeholder..."
cat > "$STYLES/session-expire.css" << 'EOF'
/* Session expiration modal styles (placeholder) */
EOF

echo "[6] Regenerating Layout.css..."
cat > "$COMPONENTS/Layout.css" << 'EOF'
.layout-container {
  display: flex;
  flex-direction: row;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: var(--bg-root);
  color: var(--text-primary);
  box-sizing: border-box;
}

.layout-main {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  min-height: 100vh;
  overflow: hidden;
  background: var(--bg-surface);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
}

.layout-content {
  flex: 1;
  width: 100%;
  min-width: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px;
  background: var(--bg-surface);
  color: var(--text-primary);
}

.layout-content::-webkit-scrollbar {
  display: none;
}
EOF

echo "[7] Regenerating Sidebar.css..."
cat > "$COMPONENTS/Sidebar.css" << 'EOF'
.sidebar {
  width: 240px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-surface);
  border-right: 1px solid var(--neon-accent-soft);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  padding: 32px 16px 20px;
  box-sizing: border-box;
  flex-shrink: 0;
  overflow: hidden;
}

.sidebar-sections {
  flex: 1;
  overflow-y: auto;
  padding-right: 4px;
}

.sidebar-sections::-webkit-scrollbar {
  display: none;
}

.sidebar-section {
  margin-bottom: 28px;
}

.sidebar-section-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.75;
}

.sidebar-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: 8px;
  color: var(--text-primary);
  text-decoration: none;
  margin-bottom: 6px;
  transition: background 0.15s ease, border-left-color 0.15s ease;
}

.sidebar-item:hover {
  background: rgba(255, 255, 255, 0.06);
}

.sidebar-item.active {
  background: rgba(255, 255, 255, 0.12);
  border-left: 3px solid var(--neon-accent);
  padding-left: 9px;
}
EOF

echo "[8] Removing legacy CSS imports from main.jsx..."
sed -i '/app.css/d' "$ROOT/src/main.jsx"

echo "[9] Running build..."
cd "$ROOT"
npm run build

echo "[10] Reloading nginx..."
sudo nginx -t && sudo systemctl reload nginx

echo "== CSS Reset Complete =="
