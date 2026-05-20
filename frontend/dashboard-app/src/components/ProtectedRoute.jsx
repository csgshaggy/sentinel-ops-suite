// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/components/ProtectedRoute.jsx

import React, { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../services/AuthContext.jsx";

/**
 * ProtectedRoute
 *
 * Ensures:
 *   - Token is restored from localStorage
 *   - AuthContext finishes initialization
 *   - User is authenticated
 *   - Redirects to https://crcybercop.dpdns.org/login only when truly unauthenticated
 *
 * Supports:
 *   - Persistent login
 *   - Admin-only panels
 *   - Session restore on refresh
 */

export default function ProtectedRoute() {
  const { isAuthenticated, authLoading, login } = useAuth();
  const [restored, setRestored] = useState(false);

  // -------------------------------------------------------
  // Restore token + user from localStorage on first load
  // -------------------------------------------------------
  useEffect(() => {
    const token = localStorage.getItem("authToken");
    const userRaw = localStorage.getItem("authUser");

    if (token && userRaw) {
      try {
        const user = JSON.parse(userRaw);

        // Hydrate AuthContext with persisted session
        login(token, user, { silent: true });
      } catch {
        console.warn("Invalid stored user JSON");
      }
    }

    setRestored(true);
  }, [login]);

  // -------------------------------------------------------
  // Still restoring session or waiting for AuthContext
  // -------------------------------------------------------
  if (!restored || authLoading) {
    return (
      <div className="route-loading-screen">
        <div className="route-loading-spinner" />
        <p>Validating session…</p>
      </div>
    );
  }

  // -------------------------------------------------------
  // No token → redirect to login
  // -------------------------------------------------------
  if (!isAuthenticated()) {
    return <Navigate to="https://crcybercop.dpdns.org/login" replace />;
  }

  // -------------------------------------------------------
  // Authenticated → allow nested routes
  // -------------------------------------------------------
  return <Outlet />;
}
