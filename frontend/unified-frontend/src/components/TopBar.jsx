import React from "react";
import { useNavigate } from "react-router-dom";
import { Bell, Settings } from "lucide-react";

import "./TopBar.css";

export default function TopBar() {
  const navigate = useNavigate();

  return (
    <header className="topbar-container">
      {/* LEFT — LOGO + TITLE */}
      <div className="topbar-left">
        <img
          src="/logo.png"   // ⭐ FIXED: correct asset path
          alt="SentinelOps Logo"
          className="topbar-logo"
        />
        <span className="topbar-title">Sentinel Ops Suite</span>
      </div>

      {/* CENTER — OPTIONAL */}
      <div className="topbar-center"></div>

      {/* RIGHT — ICON CLUSTER */}
      <div className="topbar-right">
        <div
          className="topbar-icon"
          onClick={() => navigate("/notifications")}
          aria-label="Notifications"
        >
          <Bell size={18} />
        </div>

        <img
          src="/default-avatar.png"   // ⭐ FIXED: correct asset path
          alt="User Avatar"
          className="topbar-avatar"
        />

        <div
          className="topbar-icon"
          onClick={() => navigate("/settings")}
          aria-label="Settings"
        >
          <Settings size={18} />
        </div>
      </div>
    </header>
  );
}
