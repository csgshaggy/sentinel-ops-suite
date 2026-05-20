#!/bin/bash
set -e

echo "=== UNIFIED IMPORT FIXER STARTED ==="

BASE="frontend/unified-frontend/src"

fix() {
  FILE="$1"
  FROM="$2"
  TO="$3"
  if grep -q "$FROM" "$FILE"; then
    echo "Fixing $FILE"
    sed -i "s|$FROM|$TO|g" "$FILE"
  fi
}

# ---------------------------------------
# 1. Core components + state
# ---------------------------------------
fix "$BASE/components/CommandPalette.jsx" 'commandPaletteState"' 'commandPaletteState.js"'
fix "$BASE/components/SearchBar.jsx" 'commandPaletteState"' 'commandPaletteState.js"'

fix "$BASE/components/Layout.jsx" '../components/Sidebar"' '../components/Sidebar.jsx"'
fix "$BASE/components/Layout.jsx" '../components/TopBar"' '../components/TopBar.jsx"'
fix "$BASE/components/Layout.jsx" '../components/SessionManager"' '../components/SessionManager.jsx"'

fix "$BASE/components/SentinelFooter.jsx" '../version"' '../version.js"'

# ---------------------------------------
# 2. Context + main entry
# ---------------------------------------
fix "$BASE/main.jsx" './context/AuthContext.jsx"' './features/auth/AuthContext.jsx"'

# ---------------------------------------
# 3. API + settings pages
# ---------------------------------------
fix "$BASE/pages/ForgotPassword.jsx" '../api/auth"' '../api/auth.js"'

fix "$BASE/pages/settings/MFADisable.jsx" '../../utils/axiosInstance"' '../../utils/axiosInstance.js"'
fix "$BASE/pages/settings/MFADisable.jsx" '../../features/auth/AuthContext"' '../../features/auth/AuthContext.jsx"'

fix "$BASE/pages/settings/Security.jsx" '../../utils/axiosInstance"' '../../utils/axiosInstance.js"'
fix "$BASE/pages/settings/Security.jsx" '../../features/auth/AuthContext"' '../../features/auth/AuthContext.jsx"'

# ---------------------------------------
# 4. Router + public routes
# ---------------------------------------
fix "$BASE/router.jsx" './routes/PublicRoutes"' './routes/PublicRoutes.jsx"'
fix "$BASE/router.jsx" './components/ProtectedRoute"' './components/ProtectedRoute.jsx"'
fix "$BASE/router.jsx" './components/RoleProtectedRoute"' './components/RoleProtectedRoute.jsx"'
fix "$BASE/router.jsx" './layouts/DashboardLayout"' './layouts/DashboardLayout.jsx"'
fix "$BASE/router.jsx" './pages/admin/DashboardPage"' './pages/admin/DashboardPage.jsx"'
fix "$BASE/router.jsx" './pages/admin/SecurityPage"' './pages/admin/SecurityPage.jsx"'
fix "$BASE/router.jsx" './pages/admin/UsersPage"' './pages/admin/UsersPage.jsx"'
fix "$BASE/router.jsx" './pages/admin/AuditLogsPage"' './pages/admin/AuditLogsPage.jsx"'

fix "$BASE/routes/PublicRoutes.jsx" '../pages/Login"' '../pages/Login.jsx"'

# ---------------------------------------
# 5. Admin pages (Dashboard, Security, Users, AuditLogs)
# ---------------------------------------
ADMIN="$BASE/pages/admin"

# AuditLogsPage
fix "$ADMIN/AuditLogsPage.jsx" '../../components/Layout"' '../../components/Layout.jsx"'
fix "$ADMIN/AuditLogsPage.jsx" '../../components/DashboardGrid"' '../../components/DashboardGrid.jsx"'
fix "$ADMIN/AuditLogsPage.jsx" '../../components/Panel"' '../../components/Panel.jsx"'

# DashboardPage
fix "$ADMIN/DashboardPage.jsx" '../../components/Layout"' '../../components/Layout.jsx"'
fix "$ADMIN/DashboardPage.jsx" '../../components/DashboardGrid"' '../../components/DashboardGrid.jsx"'
fix "$ADMIN/DashboardPage.jsx" '../../components/Panel"' '../../components/Panel.jsx"'
fix "$ADMIN/DashboardPage.jsx" '../../components/widgets/BackendHeartbeatWidget"' '../../components/widgets/BackendHeartbeatWidget.jsx"'
fix "$ADMIN/DashboardPage.jsx" '../../components/widgets/EnvironmentStatusWidget"' '../../components/widgets/EnvironmentStatusWidget.jsx"'
fix "$ADMIN/DashboardPage.jsx" '../../components/widgets/SandboxLogWidget"' '../../components/widgets/SandboxLogWidget.jsx"'
fix "$ADMIN/DashboardPage.jsx" '../../components/widgets/PluginRegistryWidget"' '../../components/widgets/PluginRegistryWidget.jsx"'

# SecurityPage
fix "$ADMIN/SecurityPage.jsx" '../../components/Layout"' '../../components/Layout.jsx"'
fix "$ADMIN/SecurityPage.jsx" '../../components/DashboardGrid"' '../../components/DashboardGrid.jsx"'
fix "$ADMIN/SecurityPage.jsx" '../../components/Panel"' '../../components/Panel.jsx"'
fix "$ADMIN/SecurityPage.jsx" '../../components/widgets/security/MFAStatusWidget"' '../../components/widgets/security/MFAStatusWidget.jsx"'
fix "$ADMIN/SecurityPage.jsx" '../../components/widgets/security/ActiveSessionWidget"' '../../components/widgets/security/ActiveSessionWidget.jsx"'
fix "$ADMIN/SecurityPage.jsx" '../../components/widgets/security/RBACOverviewWidget"' '../../components/widgets/security/RBACOverviewWidget.jsx"'
fix "$ADMIN/SecurityPage.jsx" '../../components/widgets/security/AuthEventStreamWidget"' '../../components/widgets/security/AuthEventStreamWidget.jsx"'

# UsersPage
fix "$ADMIN/UsersPage.jsx" '../../components/Layout"' '../../components/Layout.jsx"'
fix "$ADMIN/UsersPage.jsx" '../../components/DashboardGrid"' '../../components/DashboardGrid.jsx"'
fix "$ADMIN/UsersPage.jsx" '../../components/Panel"' '../../components/Panel.jsx"'

# ---------------------------------------
# 6. version.js (final boss)
# ---------------------------------------
fix "$BASE/version.js" 'version.txt?raw' 'version.txt'

echo "=== UNIFIED IMPORT FIXER COMPLETE ==="
