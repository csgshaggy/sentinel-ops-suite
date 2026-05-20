// frontend/src/layouts/Admin/Sidebar.tsx
// SentinelOps — Session‑Aware Sidebar

import { useContext } from "react";
import { NavLink } from "react-router-dom";
import { AuthContext } from "../../context/AuthContext";
import "./Sidebar.css";

export default function Sidebar() {
  const { user } = useContext(AuthContext);

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-title">SentinelOps</h2>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/admin/dashboard" className="sidebar-link">
          Dashboard
        </NavLink>

        <NavLink to="/admin/analytics" className="sidebar-link">
          Analytics
        </NavLink>

        <NavLink to="/admin/settings" className="sidebar-link">
          Settings
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        {user && (
          <div className="sidebar-user">
            <span className="sidebar-email">{user.email}</span>
          </div>
        )}
      </div>
    </aside>
  );
}
