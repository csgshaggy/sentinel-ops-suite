// /src/components/Sidebar.jsx
import React from "react";
import { NavLink } from "react-router-dom";
import "./Sidebar.css";

import {
  LayoutDashboard,
  ShieldCheck,
  Users,
  FileSearch,
} from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-sections">

        {/* GENERAL SECTION */}
        <div className="sidebar-section">
          <div className="sidebar-section-label">GENERAL</div>

          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              isActive ? "sidebar-item active" : "sidebar-item"
            }
          >
            <LayoutDashboard className="sidebar-icon" />
            <span className="sidebar-item-label">Dashboard</span>
          </NavLink>

          <NavLink
            to="/settings"
            className={({ isActive }) =>
              isActive ? "sidebar-item active" : "sidebar-item"
            }
          >
            <ShieldCheck className="sidebar-icon" />
            <span className="sidebar-item-label">Security</span>
          </NavLink>
        </div>

        {/* ADMIN SECTION */}
        <div className="sidebar-section">
          <div className="sidebar-section-label">ADMIN</div>

          <NavLink
            to="/admin/users"
            className={({ isActive }) =>
              isActive ? "sidebar-item active" : "sidebar-item"
            }
          >
            <Users className="sidebar-icon" />
            <span className="sidebar-item-label">User Management</span>
          </NavLink>

          <NavLink
            to="/admin/audit-logs"
            className={({ isActive }) =>
              isActive ? "sidebar-item active" : "sidebar-item"
            }
          >
            <FileSearch className="sidebar-icon" />
            <span className="sidebar-item-label">Audit Logs</span>
          </NavLink>
        </div>

      </div>
    </aside>
  );
}
