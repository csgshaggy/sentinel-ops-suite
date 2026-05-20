// File: src/routes/adminRoutes.jsx
// SentinelOps — Admin Routing Layer

import { Routes, Route, Navigate } from "react-router-dom";
import AdminDashboard from "../pages/admin/AdminDashboard";

export default function AdminRoutes() {
  return (
    <Routes>
      {/* Redirect /admin → /admin/dashboard */}
      <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />

      {/* Admin Dashboard */}
      <Route path="/admin/dashboard" element={<AdminDashboard />} />

      {/* Catch-all for unknown admin routes */}
      <Route path="/admin/*" element={<Navigate to="/admin/dashboard" replace />} />
    </Routes>
  );
}
