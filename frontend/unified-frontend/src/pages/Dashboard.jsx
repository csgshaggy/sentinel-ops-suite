// /src/pages/Dashboard.jsx
import React from "react";
import "./Dashboard.css";

export default function Dashboard() {
  const now = new Date();
  const hour = now.getHours();

  let greeting = "Hello";

  if (hour < 12) {
    greeting = "Good morning";
  } else if (hour < 18) {
    greeting = "Good afternoon";
  } else {
    greeting = "Good evening";
  }

  return (
    <div className="dashboard">

      {/* Greeting */}
      <h1 className="dashboard-greeting">
        {greeting}, Charlie
      </h1>

      {/* Neon‑glassy grid */}
      <div className="dashboard-grid">

        {/* Backend Heartbeat */}
        <div className="dash-card">
          <div className="dash-title">Backend Heartbeat</div>
          <div className="dash-line">
            <span>Status:</span>
            <span className="dash-ok">Online</span>
          </div>
          <div className="dash-line">
            <span>Latency:</span>
            <span>42ms</span>
          </div>
        </div>

        {/* Environment Status */}
        <div className="dash-card">
          <div className="dash-title">Environment Status</div>
          <div className="dash-line">
            <span>Node:</span>
            <span>v18.x</span>
          </div>
          <div className="dash-line">
            <span>Python:</span>
            <span>3.11</span>
          </div>
          <div className="dash-line">
            <span>FastAPI:</span>
            <span className="dash-ok">OK</span>
          </div>
        </div>

        {/* Sandbox Logs */}
        <div className="dash-card">
          <div className="dash-title">Sandbox Logs</div>
          <div className="dash-empty">No recent sandbox events.</div>
        </div>

        {/* Plugin Registry */}
        <div className="dash-card">
          <div className="dash-title">Plugin Registry</div>
          <div className="dash-line">
            <span>Registered Plugins:</span>
            <span>0</span>
          </div>
          <div className="dash-empty">No plugins loaded.</div>
        </div>

      </div>
    </div>
  );
}
