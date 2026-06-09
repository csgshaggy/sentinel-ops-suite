#!/bin/bash
# Sentinel Ops Suite — Avatar Renderer Patch Script (Option A)
# Patches ONLY components that actually render avatar <img> tags.

set -e

echo "🔧 Starting avatar renderer patch (Option A)..."

TARGET_FILES=$(grep -RIl --include="*.jsx" -e "<img" src/pages/Profile/components | grep -E "ProfileSummaryCard")

if [ -z "$TARGET_FILES" ]; then
    echo "❌ No avatar-rendering components found."
    exit 0
fi

echo "📄 Avatar-rendering files:"
echo "$TARGET_FILES"
echo ""

for FILE in $TARGET_FILES; do
    echo "⚙️  Patching $FILE"

    # 1. Insert import if missing
    if ! grep -q "useAvatarUrl" "$FILE"; then
        sed -i '1s|^|import useAvatarUrl from "../../../hooks/useAvatarUrl";\n|' "$FILE"
        echo "   ➕ Added useAvatarUrl import"
    fi

    # 2. Insert avatarSrc hook if missing
    if ! grep -q "const avatarSrc = useAvatarUrl" "$FILE"; then
        sed -i '/export default function/ a\
  const avatarSrc = useAvatarUrl(profile);\n' "$FILE"
        echo "   ➕ Added avatarSrc hook"
    fi

    # 3. Replace avatar <img> src with avatarSrc
    sed -i 's|<img[^>]*src={[^}]*}|<img src={avatarSrc}|g' "$FILE"
    sed -i 's|<img[^>]*src="[^"]*"|<img src={avatarSrc}|g' "$FILE"

    echo "   ✅ Patch applied"
    echo ""
done

echo "🎉 Avatar renderer patch complete!"
