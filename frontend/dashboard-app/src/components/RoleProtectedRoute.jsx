// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/components/RoleProtectedRoute.jsx

import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../services/AuthContext.jsx";

/**
 * RoleProtectedRoute
 *
 * Ensures:
 *   - AuthContext has finished loading
 *   - User is authenticated
 *   - User has the required role
 *
 * Props:
 *   - requiredRole: string
 *
 * Behavior:
 *   - Redirects to https://crcybercop.dpdns.org/login if not authenticated
 *   - Redirects to /admin if authenticated but unauthorized
 */

export default function RoleProtectedRoute({ requiredRole }) {
  const { isAuthenticated, hasRole, authLoading } = useAuth();

  // Still loading auth state
  if (authLoading) {
    return (
      <div className="route-loading-screen">
        <div className="route-loading-spinner" />
        <p>Validating session…</p>
      </div>
    );
  }

  // Not authenticated → redirect to login
  if (!isAuthenticated()) {
    return <Navigate to="https://crcybercop.dpdns.org/login" replace />;
  }

  // Authenticated but missing required role → redirect to dashboard
  if (!hasRole(requiredRole)) {
    return <Navigate to="/admin" replace />;
  }

  // Authorized → allow nested routes
  return <Outlet />;
}
