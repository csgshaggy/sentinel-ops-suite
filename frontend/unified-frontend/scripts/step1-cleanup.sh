#!/usr/bin/env bash
set -euo pipefail

echo "=== SentinelOps Frontend Cleanup — STEP 1 ONLY ==="

ROOT="src"
BACKUP="src_cleanup_backup_$(date +%s)"

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
echo "=== Removing legacy router systems ==="
move_safe "$ROOT/router.disabled"
move_safe "$ROOT/routes/AppRoutes.disabled"
move_safe "$ROOT/routes/PublicRoutes.disabled"
move_safe "$ROOT/routes"

echo ""
echo "=== Removing legacy admin system ==="
move_safe "$ROOT/pages/admin"

echo ""
echo "=== Removing legacy settings system ==="
move_safe "$ROOT/pages/settings.jsx"
move_safe "$ROOT/pages/settings"

echo ""
echo "=== Removing legacy MFA system ==="
move_safe "$ROOT/pages/MFACode.jsx"
move_safe "$ROOT/pages/MFASetup.jsx"
move_safe "$ROOT/pages/Mfa.jsx"

echo ""
echo "=== Removing legacy profile system ==="
move_safe "$ROOT/pages/profile.css"

echo ""
echo "=== Removing legacy admin panel ==="
move_safe "$ROOT/pages/AdminPanel.jsx"
move_safe "$ROOT/pages/AdminPanel.css"

echo ""
echo "=== Removing duplicate admin CSS ==="
move_safe "$ROOT/pages/AdminUsers.css"
move_safe "$ROOT/pages/AdminAuditLogs.css"

echo ""
echo "=== Removing duplicate ForgotPassword.jsx ==="
move_safe "$ROOT/pages/ForgotPassword.jsx"

echo ""
echo "=== Removing duplicate Dashboard.css ==="
move_safe "$ROOT/pages/Dashboard.css"

echo ""
echo "=== Removing .bak / .bak.patched / .disabled files ==="
find "$ROOT" -type f \( -name "*.bak" -o -name "*.bak.patched" -o -name "*.disabled" \) | while read -r file; do
    move_safe "$file"
done

echo ""
echo "=== Removing styles_backup folder ==="
move_safe "$ROOT/styles_backup_1779058139"

echo ""
echo "=== Cleanup complete ==="
echo "Backup stored in: $BACKUP"
echo "Next step: run Vite cache purge + rebuild"
