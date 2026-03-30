// =====================================================================
// SSRF Command Console — Admin Sidebar
// Collapsible • Role-Aware • Theme-Compatible
// =====================================================================

import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { useLayout } from "../../context/LayoutContext";

import "./AdminLayout.css";

export default function Sidebar() {
  const location = useLocation();
  const { user } = useAuth();
  const { sidebarCollapsed } = useLayout();

  function isActive(path: string) {
    return location.pathname.startsWith(path);
  }

  // Role-based link visibility
  const canViewUsers = user?.role === "admin" || user?.role === "operator";
  const canViewAuditLogs = user?.role === "admin";

  return (
    <aside className={`admin-sidebar ${sidebarCollapsed ? "collapsed" : ""}`}>
      <div className="admin-sidebar-title">
        {sidebarCollapsed ? "SSRF" : "SSRF Command Console"}
      </div>

      <nav>
        <ul className="admin-sidebar-nav">
          {/* Dashboard */}
          <li className={isActive("/admin/dashboard") ? "active" : ""}>
            <Link to="/admin/dashboard">{!sidebarCollapsed && "Dashboard"}</Link>
          </li>

          {/* Users (admin/operator only) */}
          {canViewUsers && (
            <>
              <li className={isActive("/admin/users") ? "active" : ""}>
                <Link to="/admin/users">{!sidebarCollapsed && "Users"}</Link>
              </li>

              <li className={isActive("/admin/users/create") ? "active" : ""}>
                <Link to="/admin/users/create">{!sidebarCollapsed && "Create User"}</Link>
              </li>
            </>
          )}

          {/* Audit Logs (admin only) */}
          {canViewAuditLogs && (
            <li className={isActive("/admin/audit-logs") ? "active" : ""}>
              <Link to="/admin/audit-logs">{!sidebarCollapsed && "Audit Logs"}</Link>
            </li>
          )}
        </ul>
      </nav>
    </aside>
  );
}
