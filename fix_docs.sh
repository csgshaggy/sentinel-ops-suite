#!/bin/bash

set -e

echo "🔍 Checking frontend/docs..."

# If frontend/docs exists but is a file, remove it
if [ -f "frontend/docs" ]; then
    echo "⚠️  frontend/docs is a FILE — removing it..."
    rm -i frontend/docs
fi

# Create correct directory structure
echo "📁 Creating documentation folder structure..."
mkdir -p frontend/docs/.vitepress

# Create index.md
echo "📝 Writing index.md..."
cat > frontend/docs/index.md << 'EOF'
# Sentinel Ops UI

Operator‑grade dashboard components for the Sentinel Ops Suite.

- Layout shell  
- Navigation  
- Status & alerts  
- Ops Console, Timeline, Heatmap  
- Theme system & tokens  
EOF

# Create components.md
echo "📝 Writing components.md..."
cat > frontend/docs/components.md << 'EOF'
# Components

## Layout
- `Layout` — shell with sidebar, status bar, breadcrumbs, command palette.

## Navigation
- `Nav` — RBAC‑aware, config‑driven.
- `MobileDrawer` — mobile slide‑in nav.

## Global UX
- `StatusBar`
- `CommandPalette`
- `NotificationCenter`
- `OpsAlerts`
- `Breadcrumbs`

## Ops
- `OpsConsole`
- `OpsTimeline`
- `OpsHeatmap`
- `OpsAssistant`
EOF

# Create theme.md
echo "📝 Writing theme.md..."
cat > frontend/docs/theme.md << 'EOF'
# Theme Tokens

See:

- `frontend/dashboard/docs/themeTokens.md`
- `frontend/dashboard/design-tokens/figma-tokens.json`
- `frontend/dashboard/styles/theme.css`
- `frontend/dashboard/styles/components.css`

These define:

- Colors  
- Typography  
- Spacing  
- Component utilities  
- CSS variables  
EOF

# Create VitePress config
echo "⚙️ Writing .vitepress/config.ts..."
cat > frontend/docs/.vitepress/config.ts << 'EOF'
import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Sentinel Ops UI",
  description: "Component library & design system for the Sentinel Ops Suite",
  themeConfig: {
    nav: [
      { text: "Overview", link: "/" },
      { text: "Components", link: "/components" },
      { text: "Theme", link: "/theme" }
    ],
    sidebar: {
      "/": [
        { text: "Overview", link: "/" },
        { text: "Components", link: "/components" },
        { text: "Theme Tokens", link: "/theme" }
      ]
    }
  }
});
EOF

echo "✅ Documentation folder repaired and populated successfully!"
echo "📚 Run 'npx vitepress dev frontend/docs' to preview your docs site."
