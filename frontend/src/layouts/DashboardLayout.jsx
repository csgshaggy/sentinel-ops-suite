// File: frontend/src/layouts/DashboardLayout.jsx
// Operator‑grade dashboard layout wrapper
// Ensures ONLY dashboard pages use the grid layout

import React from "react";
import "../index.css"; // ensures layout-root + theme variables are loaded

export default function DashboardLayout({ children }) {
  return (
    <div className="layout-root">
      {/* Sidebar */}
      <aside className="layout-sidebar">
        <div style={{ padding: "1rem", fontWeight: "bold" }}>
          SentinelOps
        </div>
        {/* You can add nav items here later */}
      </aside>

      {/* Header */}
      <header className="layout-header">
        <h3 style={{ margin: 0 }}>Analyst Console</h3>
      </header>

      {/* Main content area */}
      <main className="layout-content">
        {children}
      </main>
    </div>
  );
}
