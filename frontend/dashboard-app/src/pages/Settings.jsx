// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/pages/Settings.jsx

import React from "react";
import TopBar from "../components/TopBar";
import Sidebar from "../components/Sidebar";

import "../styles/layout.css";
import "../styles/sidebar-and-panels.css";
import "../styles/topbar.css";
import "./dashboardHome.css"; // neon theme + grid + cards

export default function Settings() {
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
              <h2 className="panel-title">System Settings</h2>
              <p className="panel-body">
                Manage preferences, configuration, and administrative controls.
              </p>
            </div>

            {/* Settings Options */}
            <div className="panel">
              <h2 className="panel-title">Available Settings</h2>

              <div className="dashboard-grid">

                <div className="dashboard-card">
                  <span className="dashboard-card-title">User Preferences</span>
                </div>

                <div className="dashboard-card">
                  <span className="dashboard-card-title">Theme Options</span>
                </div>

                <div className="dashboard-card">
                  <span className="dashboard-card-title">Access Control</span>
                </div>

                <div className="dashboard-card">
                  <span className="dashboard-card-title">System Configuration</span>
                </div>

                <div className="dashboard-card">
                  <span className="dashboard-card-title">Security Settings</span>
                </div>

              </div>
            </div>

          </div>

        </div>
      </div>
    </div>
  );
}
