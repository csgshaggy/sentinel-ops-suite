import React from "react";
import { Outlet, Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import SidebarLayout from "../../router/SidebarLayout";

const AdminLayout: React.FC = () => {
  const { authenticated, user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!authenticated || !user || user.role !== "admin") {
    return <Navigate to="/login" replace />;
  }

  return (
    <SidebarLayout>
      <Outlet />
    </SidebarLayout>
  );
};

export default AdminLayout;
