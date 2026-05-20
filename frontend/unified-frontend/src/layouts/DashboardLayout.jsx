// /home/ubuntu/sentinel-ops-suite/frontend/unified-frontend/src/layouts/DashboardLayout.jsx

import { Outlet } from "react-router-dom";
import TopBar from "../components/TopBar.jsx";
import Sidebar from "../components/Sidebar.jsx";
import SessionDebugOverlay from "../components/SessionDebugOverlay.jsx";   // <-- Added
import "../components/Layout.css";

/**
 * DashboardLayout
 *
 * Provides the unified application shell:
 *   - TopBar (user info, logout, settings)
 *   - Sidebar (navigation)
 *   - Main content area (via <Outlet />)
 *
 * Operator-mode session debug overlay added.
 */
export default function DashboardLayout() {
  return (
    <div className="app-shell">
      {/* Operator Mode Debug Overlay */}
      <SessionDebugOverlay />

      <TopBar />

      <div className="app-body">
        <Sidebar />

        <main className="app-main">
          <Outlet />   {/* <-- Correct nested route rendering */}
        </main>
      </div>
    </div>
  );
}

