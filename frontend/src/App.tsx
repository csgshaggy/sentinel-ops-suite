import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import Layout from "./layout/Layout";

import Dashboard from "./pages/Dashboard";
import Alerts from "./pages/Alerts";
import SystemHealth from "./pages/SystemHealth";
import WorkflowRuns from "./pages/WorkflowRuns";
import HealthTrend from "./pages/HealthTrend";
import HealthPredict from "./pages/HealthPredict";
import MakefileHealth from "./pages/MakefileHealth";
import RepoHealth from "./pages/RepoHealth";
import RouterDrift from "./pages/RouterDrift";
import PluginsPage from "./pages/PluginsPage";
import ObservabilityDashboard from "./pages/ObservabilityDashboard";

import PelmDashboard from "./pages/PelmDashboard";
import PelmConsole from "./pages/PelmConsole";
import PELMStatus from "./pages/PELMStatus";
import PELMTools from "./pages/PELMTools";

import LoginPage from "./pages/LoginPage";

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/system-health" element={<SystemHealth />} />
            <Route path="/workflow-runs" element={<WorkflowRuns />} />
            <Route path="/health-trend" element={<HealthTrend />} />
            <Route path="/health-predict" element={<HealthPredict />} />
            <Route path="/makefile-health" element={<MakefileHealth />} />
            <Route path="/repo-health" element={<RepoHealth />} />
            <Route path="/router-drift" element={<RouterDrift />} />
            <Route path="/plugins" element={<PluginsPage />} />
            <Route path="/observability" element={<ObservabilityDashboard />} />

            {/* Admin‑only */}
            <Route path="/pelm-dashboard" element={<ProtectedRoute role="admin"><PelmDashboard /></ProtectedRoute>} />
            <Route path="/pelm-console" element={<ProtectedRoute role="admin"><PelmConsole /></ProtectedRoute>} />
            <Route path="/pelm-status" element={<ProtectedRoute role="admin"><PELMStatus /></ProtectedRoute>} />
            <Route path="/pelm-tools" element={<ProtectedRoute role="admin"><PELMTools /></ProtectedRoute>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
