#!/bin/bash
# Sentinel Ops Suite — Global Avatar System Patch Script
# Applies Steps 3–8 automatically, safely, and idempotently.

set -e

echo "🔧 Starting Global Avatar Patch..."

###############################################
# STEP 3 — Patch AvatarTab.jsx
###############################################

AVATAR_TAB="src/pages/Profile/components/tabs/AvatarTab.jsx"

echo "⚙️  Patching AvatarTab.jsx..."

# Add import if missing
if ! grep -q "useAvatarContext" "$AVATAR_TAB"; then
  sed -i 's|import useAvatarUrl|import { useAvatarContext } from "../../../../context/AvatarContext";\nimport useAvatarUrl|' "$AVATAR_TAB"
  echo "   ➕ Added useAvatarContext import"
fi

# Add hook if missing
if ! grep -q "const { updateAvatar }" "$AVATAR_TAB"; then
  sed -i 's|const queryClient|const { updateAvatar } = useAvatarContext();\n\n  const queryClient|' "$AVATAR_TAB"
  echo "   ➕ Added updateAvatar hook"
fi

# Patch onSuccess handler
if grep -q "setOriginalAvatar(freshUrl);" "$AVATAR_TAB"; then
  sed -i 's|setOriginalAvatar(freshUrl);|updateAvatar(base, version);\n\n      setOriginalAvatar(freshUrl);|' "$AVATAR_TAB"
  echo "   ➕ Added updateAvatar(base, version) call"
fi

echo "   ✅ AvatarTab patched"


###############################################
# STEP 4 — Patch Avatar Renderers
###############################################

RENDERERS=(
  "src/components/TopBar.jsx"
  "src/components/Sidebar.jsx"
  "src/pages/Profile/components/ProfileSummaryCard.jsx"
  "src/pages/Profile/components/tabs/SessionsTab.jsx"
)

echo "⚙️  Patching avatar renderers..."

for FILE in "${RENDERERS[@]}"; do
  if [ -f "$FILE" ]; then
    echo "   ➤ $FILE"

    # Add import if missing
    if ! grep -q "useAvatarContext" "$FILE"; then
      sed -i '1s|^|import { useAvatarContext } from "../../context/AvatarContext";\n|' "$FILE"
      echo "      ➕ Added useAvatarContext import"
    fi

    # Add hook if missing
    if ! grep -q "const { avatarUrl }" "$FILE"; then
      sed -i '/function/ a\
  const { avatarUrl } = useAvatarContext();' "$FILE"
      echo "      ➕ Added avatarUrl hook"
    fi

    # Replace img src with avatarUrl
    sed -i 's|src={[^}]*}|src={avatarUrl}|g' "$FILE"
    sed -i 's|src="[^"]*"|src={avatarUrl}|g' "$FILE"

    # Remove useAvatarUrl import if present
    sed -i '/useAvatarUrl/d' "$FILE"

    echo "      ✅ Renderer patched"
  fi
done


###############################################
# STEP 5 — Add AvatarSync.jsx and inject into Layout.jsx
###############################################

SYNC_FILE="src/components/AvatarSync.jsx"

echo "⚙️  Creating AvatarSync.jsx..."

cat > "$SYNC_FILE" << 'EOF'
import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchProfile } from "../api/profileClient";
import { useAvatarContext } from "../context/AvatarContext";

export default function AvatarSync() {
  const { data: profile } = useQuery(["profile"], fetchProfile);
  const { updateAvatar } = useAvatarContext();

  useEffect(() => {
    if (!profile) return;

    const base =
      profile.avatar_thumb_url ||
      profile.avatar_url ||
      "/static/default-avatar.png";

    updateAvatar(base, profile.avatar_version);
  }, [profile]);

  return null;
}
EOF

echo "   ➕ AvatarSync.jsx created"


# Inject into Layout.jsx
LAYOUT="src/components/Layout.jsx"

if ! grep -q "AvatarSync" "$LAYOUT"; then
  sed -i '1s|^|import AvatarSync from "./AvatarSync";\n|' "$LAYOUT"
  sed -i 's|return (|return (\n    <AvatarSync />|' "$LAYOUT"
  echo "   ➕ AvatarSync injected into Layout.jsx"
fi


###############################################
# STEP 7 & 8 — Patch AvatarContext.jsx
###############################################

CONTEXT="src/context/AvatarContext.jsx"

echo "⚙️  Patching AvatarContext.jsx..."

# Add DEFAULT_AVATAR if missing
if ! grep -q "DEFAULT_AVATAR" "$CONTEXT"; then
  sed -i '1s|^|const DEFAULT_AVATAR = "/static/default-avatar.png";\n|' "$CONTEXT"
  echo "   ➕ Added DEFAULT_AVATAR"
fi

# Add preloading + fallback logic
sed -i 's|setAvatarVersion(v);|const finalUrl = baseUrl ? `${baseUrl}?v=${v}` : DEFAULT_AVATAR;\n\n    const img = new Image();\n    img.src = finalUrl;\n\n    setAvatarVersion(v);\n    setAvatarUrl(finalUrl);|' "$CONTEXT"

echo "   ✅ AvatarContext patched"


###############################################
# DONE
###############################################

echo ""
echo "🎉 Global Avatar Patch Complete!"
echo "All remaining steps have been applied automatically."
