#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="src"

echo "=== SentinelOps Frontend Cleanup ==="
echo "Cleaning legacy, duplicate, and deprecated files..."
echo

delete() {
  local path="$SRC_DIR/$1"
  if [ -e "$path" ]; then
    echo "🗑️  Removing: $path"
    rm -rf "$path"
  else
    echo "✔️  Already removed: $path"
  fi
}

echo "=== Removing legacy contexts ==="
delete "context/SessionContext.jsx"
delete "context/SettingsContext.jsx"
delete "context/ThemeContext.jsx"
delete "context/ThemeToggle.jsx"
delete "context/UserContext.jsx"

echo "=== Removing duplicate AuthContext ==="
delete "features/auth/AuthContext.jsx"

echo "=== Removing legacy MFA ==="
delete "features/auth/MFA.jsx"
delete "pages/Mfa.jsx"
delete "pages/mfa.css"

echo "=== Removing old session logic ==="
delete "components/SessionExpireModal.jsx"
delete "components/SessionExpiredModal.jsx"
delete "components/SessionExpireModal.css"
delete "components/SessionManager.jsx"
delete "managers/SessionManager.jsx"
delete "managers/SessionExpireManager.jsx"
delete "hooks/useSession.js"
delete "hooks/useSessionExpire.js"

echo "=== Removing old countdown logic ==="
delete "layouts/DashboardLayout.jsx"   # will regenerate clean

echo "=== Removing typo/duplicate route guards ==="
delete "components/RoleProtectedAoute.jsx"

echo "=== Removing old layouts ==="
delete "layouts/AdminLayout.jsx"
delete "layouts/AppShell.jsx"
delete "layouts/PublicLayout.jsx"

echo "=== Removing old routes ==="
delete "routes/AdminRoutes.sjx"
delete "routes.jsx"

echo "=== Removing legacy pages ==="
delete "pages/Systems.jsx"
delete "pages/Analytics.jsx"
delete "pages/Analytics.css"
delete "pages/Events.jsx"
delete "pages/Events.css"
delete "pages/Identity.jsx"
delete "pages/Identity.css"
delete "pages/Alerts.jsx"
delete "pages/Access.jsx"
delete "pages/Access.css"
delete "pages/Users.jsx"
delete "pages/admin"

echo "=== Removing legacy components ==="
delete "components/MfaEnrollment.jsx"
delete "components/SettingsSidebar.jsx"
delete "components/ThemeToggle.jsx"
delete "components/SessionManager.jsx"
delete "components/SessionExpireModal.jsx"
delete "components/SessionExpiredModal.jsx"

echo "=== Removing legacy managers ==="
delete "managers/RefreshManager.jsx"
delete "managers/ThemeManager.jsx"
delete "managers/UnifiedSessionOrchestrator.jsx"

echo "=== Removing legacy hooks ==="
delete "hooks/useSession.js"
delete "hooks/useSessionExpire.js"

echo "=== Removing legacy styles ==="
delete "styles/settings.css"
delete "styles/systems.css"
delete "styles/alerts.css"
delete "styles/analytics.css"
delete "styles/events.css"
delete "styles/identity.css"
delete "styles/users.css"
delete "styles/sidebar.css"
delete "styles/topbar.css"
delete "styles/panels.css"
delete "styles/forms.css"
delete "styles/buttons.css"
delete "styles/tables.css"
delete "styles/login.css"

echo
echo "=== Cleanup Complete ==="
echo "Your frontend is now ready for regeneration."
echo "Next step: regenerate the clean components/layouts/hooks."
