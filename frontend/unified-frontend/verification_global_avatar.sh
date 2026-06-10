#!/bin/bash
# Sentinel Ops Suite — Global Avatar System Verification Script (Fixed + Fast)

set -e

echo "🔍 Verifying Global Avatar System..."
PASS=true

check_has() {
  local FILE=$1
  local PATTERN=$2
  local MSG=$3

  if grep -q "$PATTERN" "$FILE"; then
    echo "   ✔ $MSG"
  else
    echo "   ❌ $MSG"
    PASS=false
  fi
}

check_missing() {
  local FILE=$1
  local PATTERN=$2
  local MSG=$3

  if grep -q "$PATTERN" "$FILE"; then
    echo "   ❌ $MSG (FOUND but should NOT be present)"
    PASS=false
  else
    echo "   ✔ $MSG"
  fi
}

###############################################
# STEP 3 — AvatarTab.jsx
###############################################

AVATAR_TAB="src/pages/Profile/components/tabs/AvatarTab.jsx"

echo ""
echo "📄 Checking AvatarTab.jsx..."

check_has "$AVATAR_TAB" "useAvatarContext" "Imports useAvatarContext"
check_has "$AVATAR_TAB" "updateAvatar" "Uses updateAvatar()"
check_has "$AVATAR_TAB" "updateAvatar(base, version)" "Calls updateAvatar(base, version)"

###############################################
# STEP 4 — Avatar Renderers
###############################################

RENDERERS=(
  "src/components/TopBar.jsx"
  "src/components/Sidebar.jsx"
  "src/pages/Profile/components/ProfileSummaryCard.jsx"
  "src/pages/Profile/components/tabs/SessionsTab.jsx"
)

echo ""
echo "📄 Checking Avatar Renderers..."

for FILE in "${RENDERERS[@]}"; do
  echo "➡ Checking $FILE"

  if [ ! -f "$FILE" ]; then
    echo "   ⚠️  File missing — skipping"
    continue
  fi

  check_has "$FILE" "useAvatarContext" "Imports useAvatarContext"
  check_has "$FILE" "avatarUrl" "Uses avatarUrl hook"
  check_has "$FILE" "src={avatarUrl}" "Renders <img src={avatarUrl}>"
  check_missing "$FILE" "useAvatarUrl" "Does NOT use useAvatarUrl"
done

###############################################
# STEP 5 — AvatarSync.jsx + Layout.jsx
###############################################

SYNC_FILE="src/components/AvatarSync.jsx"
LAYOUT="src/components/Layout.jsx"

echo ""
echo "📄 Checking AvatarSync.jsx..."

if [ -f "$SYNC_FILE" ]; then
  check_has "$SYNC_FILE" "useAvatarContext" "AvatarSync uses useAvatarContext"
  check_has "$SYNC_FILE" "fetchProfile" "AvatarSync fetches profile"
  check_has "$SYNC_FILE" "updateAvatar" "AvatarSync calls updateAvatar"
else
  echo "   ❌ AvatarSync.jsx missing"
  PASS=false
fi

echo ""
echo "📄 Checking Layout.jsx..."

check_has "$LAYOUT" "AvatarSync" "Layout imports AvatarSync"
check_has "$LAYOUT" "<AvatarSync" "Layout renders <AvatarSync />"

###############################################
# STEP 7 & 8 — AvatarContext.jsx
###############################################

CONTEXT="src/context/AvatarContext.jsx"

echo ""
echo "📄 Checking AvatarContext.jsx..."

check_has "$CONTEXT" "DEFAULT_AVATAR" "Has DEFAULT_AVATAR fallback"
check_has "$CONTEXT" "new Image()" "Preloads avatar images"
check_has "$CONTEXT" "setAvatarUrl" "Updates avatarUrl"
check_has "$CONTEXT" "setAvatarVersion" "Updates avatarVersion"

###############################################
# FINAL RESULT
###############################################

echo ""
if [ "$PASS" = true ]; then
  echo "🎉 ALL CHECKS PASSED — Global Avatar System is correctly wired!"
else
  echo "❌ SOME CHECKS FAILED — Review the output above."
  exit 1
fi
