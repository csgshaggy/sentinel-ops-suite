#!/usr/bin/env bash
set -euo pipefail

echo "=== SentinelOps Frontend Cleanup — STEP 2 (Mode A: Conservative) ==="

ROOT="src"
BACKUP="src_unused_components_backup_$(date +%s)"

echo "Creating backup folder: $BACKUP"
mkdir -p "$BACKUP"

move_safe() {
    local target="$1"
    if [ -e "$target" ]; then
        echo "Moving: $target → $BACKUP/"
        mv "$target" "$BACKUP/"
    else
        echo "Skipping (not found): $target"
    fi
}

echo ""
echo "=== Removing leftover .bak / .bak.patched / .disabled files ==="
find "$ROOT" -type f \( -name "*.bak" -o -name "*.bak.patched" -o -name "*.disabled" \) | while read -r file; do
    move_safe "$file"
done

echo ""
echo "=== Removing known ghost components ==="
move_safe "$ROOT/components/SessionEvenTimeline.jsx"

echo ""
echo "=== Removing legacy MFA components (not used by AuthContext) ==="
move_safe "$ROOT/pages/MFACode.jsx"
move_safe "$ROOT/pages/MFASetup.jsx"
move_safe "$ROOT/pages/Mfa.jsx"

echo ""
echo "=== Removing legacy profile components (App.jsx uses pages/Profile only) ==="
move_safe "$ROOT/components/profile"

echo ""
echo "=== Removing legacy settings components (App.jsx uses pages/settings only) ==="
move_safe "$ROOT/components/settings"

echo ""
echo "=== Removing components belonging to deleted pages ==="
move_safe "$ROOT/components/providers/SettingsFooter.jsx"  # from old settings system
move_safe "$ROOT/components/providers/SettingsTabs.css"    # from old settings system

echo ""
echo "=== Removing unused admin widgets (legacy admin system removed in Step 1) ==="
move_safe "$ROOT/components/widgets/audit"
move_safe "$ROOT/components/widgets/users"
move_safe "$ROOT/components/widgets/security"
move_safe "$ROOT/components/widgets/sessions"

echo ""
echo "=== Cleanup complete ==="
echo "Backup stored in: $BACKUP"
echo "Next step: purge Vite cache + rebuild"
