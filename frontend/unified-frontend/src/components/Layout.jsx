import AvatarSync from "./AvatarSync";
// /src/components/Layout.jsx
import React, { memo } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar.jsx";
import TopBar from "./TopBar.jsx";
import SentinelFooter from "./SentinelFooter.jsx";

import useInactivityLogout from "../hooks/useInactivityLogout.js";
import { useAuth } from "../features/auth/AuthContext.jsx";

import "./Layout.css";

function Layout() {
  const { logout } = useAuth();

  // Inactivity logout (15m timeout, 3m warning)
  useInactivityLogout({
    timeoutMinutes: 15,
    warningMinutes: 3,
    onExpire: logout,
  });

  return (
    <AvatarSync />
    <div className="layout-container">
      {/* Sidebar (left) */}
      <Sidebar />

      {/* Main content column */}
      <div className="layout-main">
        {/* TopBar (normal flow, no fixed positioning) */}
        <TopBar />

        {/* Routed content */}
        <main className="layout-content">
          <Outlet />
        </main>

        {/* Footer */}
        <SentinelFooter />
      </div>
    </div>
  );
}

export default memo(Layout);
