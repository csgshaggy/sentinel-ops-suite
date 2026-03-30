// =====================================================================
// SSRF Command Console — Application Routes
// Unified Admin Layout • Session Cookie Auth • TypeScript
// =====================================================================

import { Routes, Route } from "react-router-dom";

// Admin Layout (new normalized path)
import AdminLayout from "../layouts/Admin/AdminLayout";

// Admin Pages
import AdminDashboard from "../pages/admin/AdminDashboard";
import AdminUsers from "../pages/admin/AdminUsers";
import AdminUserCreate from "../pages/admin/AdminUserCreate";
import AdminUserEdit from "../pages/admin/AdminUserEdit";
import AdminAuditLogs from "../pages/admin/AdminAuditLogs";

// Public Pages
import LoginPage from "../pages/LoginPage";

export default function AppRoutes() {
  return (
    <Routes>

      {/* Public */}
      <Route path="/login" element={<LoginPage />} />

      {/* Admin Console */}
      <Route path="/admin" element={<AdminLayout />}>
        <Route path="dashboard" element={<AdminDashboard />} />
        <Route path="users" element={<AdminUsers />} />
        <Route path="users/create" element={<AdminUserCreate />} />
        <Route path="users/:id" element={<AdminUserEdit />} />
        <Route path="audit-logs" element={<AdminAuditLogs />} />
      </Route>

    </Routes>
  );
}
