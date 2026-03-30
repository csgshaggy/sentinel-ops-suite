// =====================================================================
// SSRF Command Console — Admin Topbar
// Breadcrumbs • Theme Toggle • Sidebar Collapse • Logout
// =====================================================================

import { useAuth } from "../../context/AuthContext";
import { useLayout } from "../../context/LayoutContext";
import { useTheme } from "../../context/ThemeContext";

import Breadcrumbs from "../../components/Breadcrumbs";

import "./AdminLayout.css";

export default function Topbar() {
  const { logout, user } = useAuth();
  const { sidebarCollapsed, setSidebarCollapsed } = useLayout();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="admin-topbar">
      <div className="admin-topbar-left">
        {/* Sidebar collapse toggle */}
        <button
          className="sidebar-toggle"
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
        >
          {sidebarCollapsed ? "☰" : "⮜"}
        </button>

        {/* Breadcrumbs */}
        <Breadcrumbs />
      </div>

      <div className="admin-topbar-right">
        {/* Theme toggle */}
        <button onClick={toggleTheme}>{theme === "dark" ? "🌙" : "☀️"}</button>

        {/* User role indicator */}
        {user && <span className="topbar-role">{user.role.toUpperCase()}</span>}

        {/* Logout */}
        <button onClick={logout}>Logout</button>
      </div>
    </header>
  );
}
