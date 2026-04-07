// File: /home/ubuntu/sentinel-ops-suite/frontend/src/routes/AppRoutes.tsx

import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import AdminDashboard from "../pages/AdminDashboard";
import MfaChallenge from "../pages/MfaChallenge";

// ✅ Corrected imports — these were the root cause
import ProtectedRoute from "../components/ProtectedRoute";

import DashboardLayout from "../layouts/DashboardLayout";

console.log("APP_ROUTES_LOADED");

export default function AppRoutes() {
  return (
    <Routes>
      {/* ----------------------------- */}
      {/* PUBLIC ROUTES                 */}
      {/* ----------------------------- */}
      <Route path="/login" element={<Login />} />
      <Route path="/mfa" element={<MfaChallenge />} />

      {/* ----------------------------- */}
      {/* PROTECTED ROUTES              */}
      {/* ----------------------------- */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <Dashboard />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin"
        element={
          <ProtectedRoute role="admin">
            <DashboardLayout>
              <AdminDashboard />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* ----------------------------- */}
      {/* DEFAULT ROUTE (FIXED)         */}
      {/* ----------------------------- */}
      <Route index element={<Navigate to="/dashboard" replace />} />

      {/* ----------------------------- */}
      {/* CATCH-ALL → LOGIN             */}
      {/* ----------------------------- */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
