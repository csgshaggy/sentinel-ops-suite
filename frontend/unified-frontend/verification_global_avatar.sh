#!/bin/bash
# Sentinel Ops Suite — Global Avatar System Verification Script
# Verifies Steps 3–8 are correctly applied.

set -e

echo "🔍 Verifying Global Avatar System..."

PASS=true

check_file_contains() {
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

###############################################
# STEP 3 — Verify AvatarTab.jsx
###############################################

AVATAR_TAB="src/pages/Profile/components/tabs/AvatarTab.jsx"

echo ""
echo "📄 Checking AvatarTab.jsx..."

check_file_contains "$AVATAR_TAB" "useAvatarContext" "Imports useAvatarContext"
check_file_contains "$AVATAR_TAB" "updateAvatar" "Uses updateAvatar()"
check_file_contains "$AVATAR_TAB" "updateAvatar(base, version)" "Calls updateAvatar(base, version)"


###############################################
# STEP 4 — Verify Avatar Renderers
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
  if [ -f "$FILE" ]; then
    echo "➡ $FILE"

    check_file_contains "$FILE" "useAvatarContext" "Imports useAvatarContext"
    check_file_contains "$FILE" "avatarUrl" "Uses avatarUrl hook"
    check_file_contains "$FILE" "src={avatarUrl}" "Renders <img src={avatarUrl}>"
    check_file_contains "$FILE" -v "useAvatarUrl" "Does NOT use useAvatarUrl"
  fi
done


###############################################
# STEP 5 — Verify AvatarSync.jsx and Layout.jsx
###############################################

SYNC_FILE="src/components/AvatarSync.jsx"
LAYOUT="src/components/Layout.jsx"

echo ""
echo "📄 Checking AvatarSync.jsx..."

if [ -f "$SYNC_FILE" ]; then
  check_file_contains "$SYNC_FILE" "useAvatarContext" "AvatarSync uses useAvatarContext"
  check_file_contains "$SYNC_FILE" "fetchProfile" "AvatarSync fetches profile"
  check_file_contains "$SYNC_FILE" "updateAvatar" "AvatarSync calls updateAvatar"
else
  echo "   ❌ AvatarSync.jsx missing"
  PASS=false
fi

echo ""
echo "📄 Checking Layout.jsx..."

check_file_contains "$LAYOUT" "AvatarSync" "Layout imports AvatarSync"
check_file_contains "$LAYOUT" "<AvatarSync" "Layout renders <AvatarSync />"


###############################################
# STEP 7 & 8 — Verify AvatarContext.jsx
###############################################

CONTEXT="src/context/AvatarContext.jsx"

echo ""
echo "📄 Checking AvatarContext.jsx..."

check_file_contains "$CONTEXT" "DEFAULT_AVATAR" "Has DEFAULT_AVATAR fallback"
check_file_contains "$CONTEXT" "new Image()" "Preloads avatar images"
check_file_contains "$CONTEXT" "setAvatarUrl" "Updates avatarUrl"
check_file_contains "$CONTEXT" "setAvatarVersion" "Updates avatarVersion"


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

