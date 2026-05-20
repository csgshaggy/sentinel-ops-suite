// frontend/dashboard-app/src/ProtectedRoute.jsx

import React from "react";
import { Navigate } from "react-router-dom";

/**
 * ProtectedRoute
 * Enforces authentication for all dashboard routes.
 *
 * Requirements:
 *   - login-app stores "authToken" containing the backend's access_token
 *   - dashboard-app must validate this before rendering protected content
 *
 * Behavior:
 *   - If token missing/null/undefined → redirect to "/login"
 *   - If token exists → allow access to protected children
 */

export default function ProtectedRoute({ children }) {
  const token =
    localStorage.getItem("authToken") ||
    sessionStorage.getItem("authToken");

  // Harden against literal "null" or "undefined" strings
  if (!token || token === "null" || token === "undefined") {
    return <Navigate to="/login" replace />;
  }

  return children;
}
