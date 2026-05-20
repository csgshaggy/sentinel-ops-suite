// src/components/layout/Sidebar.jsx

import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../../services/AuthContext.jsx";
import { useSettings } from "../../services/SettingsContext.jsx";

import "../../styles/sidebar.css";

export default function Sidebar({ onOpenSettings }) {
  const { user, roles, hasRole, hasAnyRole } = useAuth();
  const { settings } = useSettings();

  const [drawerOpen, setDrawerOpen] = useState(false);
  const [openGroup, setOpenGroup] = useState(null);

  if (!settings) return null;

  const {
    sidebar_collapsed,
    show_profile,
    display_name,
  } = settings;

  const toggleGroup = (group) => {
    setOpenGroup((prev) => (prev === group ? null : group));
  };

  const closeDrawer = () => setDrawerOpen(false);

  return (
    <>
      {/* MOBILE BACKDROP */}
      <div
        className={`sidebar-backdrop ${drawerOpen ? "open" : ""}`}
        onClick={closeDrawer}
      />

      {/* SIDEBAR */}
      <aside
        className={`sidebar ${sidebar_collapsed ? "collapsed" : ""} ${
          drawerOpen ? "open" : ""
        }`}
      >
        {/* TITLE */}
        <div className="sidebar-title">Sentinel Ops</div>

        {/* PROFILE BLOCK (settings-controlled) */}
        {show_profile && (
          <div className="sidebar-profile">
            <div className="avatar" />
            <div className="profile-name">
              {display_name || user?.username || "User"}
            </div>
          </div>
        )}

        {/* NAVIGATION */}
        <nav className="sidebar-nav">

          {/* DASHBOARD */}
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `sidebar-item ${isActive ? "active" : ""}`
            }
            onClick={closeDrawer}
          >
            <span className="icon">📊</span>
            <span className="sidebar-label">Dashboard</span>
          </NavLink>

          {/* ALERTS */}
          <NavLink
            to="/alerts"
            className={({ isActive }) =>
              `sidebar-item ${isActive ? "active" : ""}`
            }
            onClick={closeDrawer}
          >
            <span className="icon">🚨</span>
            <span className="sidebar-label">Alerts</span>
          </NavLink>

          {/* ANALYTICS */}
          <NavLink
            to="/analytics"
            className={({ isActive }) =>
              `sidebar-item ${isActive ? "active" : ""}`
            }
            onClick={closeDrawer}
          >
            <span className="icon">📈</span>
            <span className="sidebar-label">Analytics</span>
          </NavLink>

          {/* SYSTEMS & MODULES — EXPANDABLE GROUP */}
          <div
            className={`sidebar-item ${openGroup === "systems" ? "open" : ""}`}
            onClick={() => toggleGroup("systems")}
          >
            <span className="icon">🧩</span>
            <span className="sidebar-label">Systems & Modules</span>
            <span className="sidebar-chevron">▶</span>
          </div>

          <div
            className={`sidebar-submenu ${
              openGroup === "systems" ? "open" : ""
            }`}
          >
            <NavLink
              to="/systems/overview"
              className="sidebar-subitem"
              onClick={closeDrawer}
            >
              Overview
            </NavLink>

            <NavLink
              to="/systems/modules"
              className="sidebar-subitem"
              onClick={closeDrawer}
            >
              Modules
            </NavLink>
          </div>

          {/* SETTINGS (RBAC: only admins) */}
          {hasRole("admin") && (
            <NavLink
              to="/settings"
              className={({ isActive }) =>
                `sidebar-item ${isActive ? "active" : ""}`
              }
              onClick={closeDrawer}
            >
              <span className="icon">⚙️</span>
              <span className="sidebar-label">Settings</span>
            </NavLink>
          )}
        </nav>

        {/* SETTINGS BUTTON (opens modal) */}
        <button className="settings-btn" onClick={onOpenSettings}>
          Preferences
        </button>
      </aside>

      {/* MOBILE MENU BUTTON */}
      <button
        className="mobile-menu-button"
        onClick={() => setDrawerOpen(true)}
      >
        ☰
      </button>
    </>
  );
}
