// /src/components/Layout.jsx
import React from "react";
import { Outlet, useOutletContext } from "react-router-dom";

import Sidebar from "./Sidebar";
import TopBar from "./TopBar";
import SentinelFooter from "./SentinelFooter";

import useInactivityLogout from "../hooks/useInactivityLogout.js";
import { useAuth } from "../features/auth/AuthContext.jsx";

import "./Layout.css";

export default function Layout() {
  const { user } = useOutletContext() || {};
  const { logout } = useAuth();

  // ⏳ Enforce 15‑minute inactivity logout with 3‑minute warning
  useInactivityLogout({
    timeoutMinutes: 15,
    warningMinutes: 3,
    onExpire: logout,
  });

  return (
    <div className="layout-container">
      <Sidebar />

      <div className="layout-main">
        <TopBar user={user} />

        <main className="layout-content">
          <Outlet />
        </main>

        <SentinelFooter />
      </div>
    </div>
  );
}
