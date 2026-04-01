import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Core pages
import Dashboard from "./pages/Dashboard";

// Health & Observability
import HealthScore from "./pages/HealthScore";
import HealthTrend from "./pages/HealthTrend";
import HealthPredict from "./pages/HealthPredict";

// Anomalies
import AnomalyCorrelation from "./pages/AnomalyCorrelation";

// Alerts
import Alerts from "./pages/Alerts";

// Makefile Governance
import MakefileDashboardPage from "./pages/MakefileDashboardPage";

// PELM
import PelmHealth from "./pages/PelmHealth";
import PelmStream from "./pages/PelmStream";

// Layout
import Sidebar from "./components/Sidebar";

export default function App() {
  return (
    <Router>
      <div style={{ display: "flex", height: "100vh" }}>
        <Sidebar />

        <div style={{ flex: 1, overflowY: "auto" }}>
          <Routes>
            {/* Dashboard */}
            <Route path="/" element={<Dashboard />} />

            {/* Health */}
            <Route path="/health-score" element={<HealthScore />} />
            <Route path="/health-trend" element={<HealthTrend />} />
            <Route path="/health-predict" element={<HealthPredict />} />

            {/* Anomalies */}
            <Route path="/anomaly-correlation" element={<AnomalyCorrelation />} />

            {/* Alerts */}
            <Route path="/alerts" element={<Alerts />} />

            {/* Makefile Governance */}
            <Route path="/makefile-dashboard" element={<MakefileDashboardPage />} />

            {/* PELM */}
            <Route path="/pelm-health" element={<PelmHealth />} />
            <Route path="/pelm-stream" element={<PelmStream />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}
