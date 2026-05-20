// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/pages/Alerts.jsx

import React from "react";
import TopBar from "../components/TopBar";
import Sidebar from "../components/Sidebar";

import "../styles/layout.css";
import "../styles/sidebar-and-panels.css";
import "../styles/topbar.css";
import "./dashboardHome.css"; // for grid + neon theme

export default function Alerts() {
  return (
    <div className="layout-root">

      {/* Fixed TopBar */}
      <TopBar />

      {/* Mobile/desktop hybrid Sidebar */}
      <Sidebar />

      {/* Main content area */}
      <div className="layout-main">
        <div className="layout-content">

          <div className="panel-shell">

            {/* Header Panel */}
            <div className="panel">
              <h2 className="panel-title">Alerts Center</h2>
              <p className="panel-body">
                Review system alerts, warnings, and operational signals.
              </p>
            </div>

            {/* Alerts List Panel */}
            <div className="panel">
              <h2 className="panel-title">Active Alerts</h2>

              <div className="dashboard-grid">
                <div className="dashboard-card">
                  <span className="dashboard-card-title">No active alerts</span>
                </div>
              </div>
            </div>

          </div>

        </div>
      </div>
    </div>
  );
}
