#!/bin/bash
# Sentinel Ops Suite — Global Avatar Patch Script (Step 1)
# Patches all avatar-rendering components to use useAvatarUrl()

set -e

ROOT="src"
HOOK_IMPORT='import useAvatarUrl from "../../hooks/useAvatarUrl";'
HOOK_IMPORT_DEEP='import useAvatarUrl from "../../../hooks/useAvatarUrl";'
HOOK_IMPORT_DEEPER='import useAvatarUrl from "../../../../hooks/useAvatarUrl";'

echo "🔧 Starting global avatar patch..."

# 1. Find all files that reference avatar_url or avatar_thumb_url
FILES=$(grep -RIl --include="*.jsx" -e "avatar_url" -e "avatar_thumb_url" "$ROOT")

if [ -z "$FILES" ]; then
    echo "No avatar-rendering components found."
    exit 0
fi

echo "📄 Files to patch:"
echo "$FILES"
echo ""

for FILE in $FILES; do
    echo "⚙️  Patching $FILE"

    # Determine correct import depth
    if grep -q "src/pages/Profile" <<< "$FILE"; then
        IMPORT="$HOOK_IMPORT_DEEPER"
    elif grep -q "src/components" <<< "$FILE"; then
        IMPORT="$HOOK_IMPORT"
    else
        IMPORT="$HOOK_IMPORT_DEEP"
    fi

    # 2. Insert useAvatarUrl import if missing
    if ! grep -q "useAvatarUrl" "$FILE"; then
        sed -i "1s/^/$IMPORT\n/" "$FILE"
        echo "   ➕ Added useAvatarUrl import"
    fi

    # 3. Replace direct avatar_url usage with avatarSrc
    sed -i 's/profile\.avatar_url/avatarSrc/g' "$FILE"
    sed -i 's/profile\.avatar_thumb_url/avatarSrc/g' "$FILE"
    sed -i 's/user\.avatar_url/avatarSrc/g' "$FILE"
    sed -i 's/user\.avatar_thumb_url/avatarSrc/g' "$FILE"
    sed -i 's/session\.user\.avatar_url/avatarSrc/g' "$FILE"
    sed -i 's/session\.user\.avatar_thumb_url/avatarSrc/g' "$FILE"

    # 4. Insert avatarSrc hook if not present
    if ! grep -q "const avatarSrc = useAvatarUrl" "$FILE"; then
        # Insert after first import block
        sed -i '/import/{:a;N;/\n[^ ]/!ba};/import/!b; s/$/\n\nconst avatarSrc = useAvatarUrl(profile || user || session?.user);/' "$FILE"
        echo "   ➕ Added avatarSrc hook"
    fi

    # 5. Replace <img src=...> with <img src={avatarSrc}>
    sed -i 's/src={[^}]*}/src={avatarSrc}/g' "$FILE"
    sed -i 's/src="[^"]*"/src={avatarSrc}/g' "$FILE"

    echo "   ✅ Patch applied"
    echo ""
done

echo "🎉 Global avatar patch complete!"
