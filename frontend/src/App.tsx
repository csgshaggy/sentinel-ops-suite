import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import ConsoleMenu from "./components/ConsoleMenu";
import ActionPanel from "./components/ActionPanel";

// Pages
import Dashboard from "./pages/Dashboard";
import Logs from "./pages/Logs";
import Anomalies from "./pages/Anomalies";
import Health from "./pages/Health";
import HealthScore from "./pages/HealthScore";
import HealthTrend from "./pages/HealthTrend";
import PelmDashboard from "./pages/PelmDashboard";

export default function App() {
  return (
    <Router>
      <div style={{ display: "flex", height: "100vh" }}>
        <ConsoleMenu />

        <div style={{ flex: 1, overflowY: "auto" }}>
          <ActionPanel />

          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/logs" element={<Logs />} />
            <Route path="/anomalies" element={<Anomalies />} />
            <Route path="/health" element={<Health />} />
            <Route path="/health-score" element={<HealthScore />} />
            <Route path="/health-trend" element={<HealthTrend />} />
            <Route path="/pelm" element={<PelmDashboard />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}
