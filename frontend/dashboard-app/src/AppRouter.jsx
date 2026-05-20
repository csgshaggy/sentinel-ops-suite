// src/AppRouter.jsx

import { useEffect } from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";

import Layout from "./components/layout/Layout.jsx";
import { useAuth } from "./services/AuthContext.jsx";
import { useSettings } from "./services/SettingsContext.jsx";

import Dashboard from "./pages/Dashboard.jsx";
import Alerts from "./pages/Alerts.jsx";
import Analytics from "./pages/Analytics.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";

export default function AppRouter() {
  const { isAuthenticated } = useAuth();
  const { settings, loading } = useSettings();
  const navigate = useNavigate();

  // Redirect user to their landing page after login
  useEffect(() => {
    if (!loading && isAuthenticated && settings) {
      navigate(`/${settings.landing_page}`, { replace: true });
    }
  }, [loading, isAuthenticated, settings, navigate]);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (loading || !settings) {
    return <div className="loading-screen">Loading user settings…</div>;
  }

  return (
    <Layout>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/settings" element={<SettingsPage />} />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Layout>
  );
}
