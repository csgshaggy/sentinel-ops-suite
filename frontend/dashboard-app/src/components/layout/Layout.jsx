// src/components/layout/Layout.jsx

import React, { useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar.jsx";
import TopBar from "./TopBar.jsx";
import ThemeManager from "./ThemeManager.jsx";
import ToastManager from "./ToastManager.jsx";
import RefreshManager from "./RefreshManager.jsx";

import SettingsModal from "../settings/SettingsModal.jsx"
import { useSettings } from "../../context/SettingsContext.jsx";

import "../../styles/layout.css";
import "../../styles/sidebar.css";
import "../../styles/topbar.css";

export default function Layout() {
  const { settings } = useSettings();
  const [settingsOpen, setSettingsOpen] = useState(false);

  if (!settings) return null;

  const { sidebar_collapsed } = settings;
  const rootClass = sidebar_collapsed
    ? "layout-root sidebar-collapsed"
    : "layout-root";

  return (
    <>
      {/* Global managers */}
      <ThemeManager />
      <ToastManager />
      <RefreshManager />

      {/* Settings modal */}
      <SettingsModal
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
      />

      <div className={rootClass}>
        {/* TOP BAR */}
        <div className="layout-topbar">
          <TopBar onOpenSettings={() => setSettingsOpen(true)} />
        </div>

        {/* SIDEBAR */}
        <div className="layout-sidebar">
          <Sidebar
            collapsed={sidebar_collapsed}
            onOpenSettings={() => setSettingsOpen(true)}
          />
        </div>

        {/* MAIN CONTENT */}
        <main className="layout-content">
          <Outlet />
        </main>
      </div>
    </>
  );
}
