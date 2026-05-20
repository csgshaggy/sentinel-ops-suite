import React, { useState } from "react";
import { Outlet } from "react-router-dom";

import TopBar from "./components/TopBar.jsx";
import Sidebar from "./components/Sidebar.jsx";
import SettingsModal from "./components/SettingsModal.jsx";

import "./styles/layout.css";

export default function Layout() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className={`layout-root ${collapsed ? "collapsed" : ""}`}>

      {/* SIDEBAR — collapsible, neon-glass */}
      <Sidebar collapsed={collapsed} />

      {/* MAIN COLUMN */}
      <div className="layout-main">

        {/* TOP BAR — centered content, collapse-aware */}
        <TopBar collapsed={collapsed} setCollapsed={setCollapsed} />

        {/* SETTINGS MODAL — portal-based */}
        <SettingsModal />

        {/* ROUTE CONTENT */}
        <main className="layout-content">
          <Outlet />
        </main>

      </div>
    </div>
  );
}
