// frontend/src/pages/Dashboard.jsx

import React from "react";
import "./Dashboard.css";

export default function Dashboard() {
  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">SentinelOps Analyst Dashboard</h1>

      <div className="dashboard-welcome">
        <p>Welcome to the operational dashboard.</p>
        <p>Your tiles, alerts, and system metrics will appear here.</p>
      </div>

      <div className="dashboard-placeholder">
        <p>Dashboard shell loaded successfully.</p>
        <p>Data wiring begins in Item 3.</p>
      </div>
    </div>
  );
}
