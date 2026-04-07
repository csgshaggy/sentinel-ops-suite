// File: /home/ubuntu/sentinel-ops-suite/frontend/src/layouts/Admin/AdminLayout.tsx

import React from "react";
import { Navigate, Outlet } from "react-router-dom";

// ✅ Corrected import — now using the real AuthContext
import { useAuth } from "../../context/AuthContext";

import AdminSidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function AdminLayout() {
  const { user } = useAuth();

  // Only allow admin users into this layout
  if (!user || user.role !== "admin") {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="admin-layout">
      <Topbar />
      <div className="admin-body">
        <AdminSidebar />
        <main className="admin-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
