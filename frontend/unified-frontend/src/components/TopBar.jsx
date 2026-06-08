import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Bell, Settings } from "lucide-react";

import "./TopBar.css";

export default function TopBar() {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="topbar-container">
      {/* LEFT — LOGO + TITLE */}
      <div className="topbar-left">
        <img
          src="/logo.png"
          alt="SentinelOps Logo"
          className="topbar-logo"
        />
        <span className="topbar-title">Sentinel Ops Suite</span>
      </div>

      {/* CENTER — OPTIONAL */}
      <div className="topbar-center"></div>

      {/* RIGHT — ICON CLUSTER */}
      <div className="topbar-right">
        {/* Notifications */}
        <div
          className="topbar-icon"
          onClick={() => navigate("/notifications")}
          aria-label="Notifications"
        >
          <Bell size={18} />
        </div>

        {/* Avatar + Dropdown */}
        <div className="avatar-wrapper">
          <img
            src="/default-avatar.png"
            alt="User Avatar"
            className="topbar-avatar"
            onClick={() => setMenuOpen(!menuOpen)}
          />

          {/* Dropdown Menu */}
          {menuOpen && (
            <div className="avatar-dropdown">
              <div
                className="dropdown-item"
                onClick={() => navigate("/profile")}
              >
                Profile
              </div>

              <div
                className="dropdown-item"
                onClick={() => navigate("/settings")}
              >
                <Settings size={16} style={{ marginRight: "8px" }} />
                Settings
              </div>

              <div
                className="dropdown-item"
                onClick={() => navigate("/logout")}
              >
                Logout
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
