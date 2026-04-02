import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import AdminLayout from "../layouts/Admin/AdminLayout";
import AdminAuditLogs from "../pages/admin/AdminAuditLogs";
import AdminDashboard from "../pages/admin/AdminDashboard";
import AdminUserCreate from "../pages/admin/AdminUserCreate";
import AdminUserEdit from "../pages/admin/AdminUserEdit";
import AdminUsers from "../pages/admin/AdminUsers";
import MfaChallenge from "../pages/auth/MfaChallenge";
import LoginPage from "../pages/LoginPage";
import MfaEnrollment from "../pages/settings/MfaEnrollment";
import MfaSettings from "../pages/settings/MfaSettings";

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/auth/mfa" element={<MfaChallenge />} />

      <Route path="/settings/mfa" element={<MfaSettings />} />
      <Route path="/settings/mfa/enroll" element={<MfaEnrollment />} />

      <Route path="/admin" element={<AdminLayout />}>
        <Route index element={<AdminDashboard />} />
        <Route path="users" element={<AdminUsers />} />
        <Route path="users/create" element={<AdminUserCreate />} />
        <Route path="users/:id/edit" element={<AdminUserEdit />} />
        <Route path="audit-logs" element={<AdminAuditLogs />} />
      </Route>

      <Route path="*" element={<Navigate to="/admin" replace />} />
    </Routes>
  );
};

export default AppRoutes;
