// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/pages/Analytics.jsx

import React from "react";
import TopBar from "../components/TopBar";
import Sidebar from "../components/Sidebar";

import "../styles/layout.css";
import "../styles/sidebar-and-panels.css";
import "../styles/topbar.css";
import "./dashboardHome.css"; // neon theme + grid + cards

export default function Analytics() {
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
              <h2 className="panel-title">Analytics Dashboard</h2>
              <p className="panel-body">
                Explore system metrics, performance indicators, and operational insights.
              </p>
            </div>

            {/* Analytics Panels */}
            <div className="panel">
              <h2 className="panel-title">Available Analytics</h2>

              <div className="dashboard-grid">

                <div className="dashboard-card">
                  <span className="dashboard-card-title">System Metrics</span>
                </div>

                <div className="dashboard-card">
                  <span className="dashboard-card-title">Performance Trends</span>
                </div>

                <div className="dashboard-card">
                  <span className="dashboard-card-title">Event Correlation</span>
                </div>

                <div className="dashboard-card">
                  <span className="dashboard-card-title">Threat Intelligence</span>
                </div>

              </div>
            </div>

          </div>

        </div>
      </div>
    </div>
  );
}
