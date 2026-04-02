// frontend/src/App.tsx

import React from "react";
import { BrowserRouter as Router, Link, Navigate,Route, Routes } from "react-router-dom";

import PelmConsole from "./pages/PelmConsole";
import PelmDashboard from "./pages/PelmDashboard";

export default function App() {
  return (
    <Router>
      <div
        style={{
          padding: "10px 20px",
          background: "#111",
          marginBottom: 20,
          display: "flex",
          gap: 20,
        }}
      >
        <Link to="/pelm/console" style={{ color: "#fff", textDecoration: "none" }}>
          PELM Console
        </Link>
        <Link to="/pelm/dashboard" style={{ color: "#fff", textDecoration: "none" }}>
          PELM Governance Dashboard
        </Link>
      </div>

      <Routes>
        <Route path="/" element={<Navigate to="/pelm/console" replace />} />
        <Route path="/pelm/console" element={<PelmConsole />} />
        <Route path="/pelm/dashboard" element={<PelmDashboard />} />
      </Routes>
    </Router>
  );
}
