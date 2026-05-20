// /src/components/RoleProtectedRoute.jsx

import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { toast } from "./ToastManager.jsx";

/**
 * RoleProtectedRoute
 *
 * Ensures:
 *   - AuthContext has completed session restore
 *   - User is authenticated
 *   - User has one of the allowed roles
 *   - Redirects to /login if unauthenticated
 *   - Redirects to / if authenticated but unauthorized
 *   - No inline UI (toast-only migration)
 */
export default function RoleProtectedRoute({
  allowedRoles = [],
  children,
  onError,
}) {
  const { user, isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // Still restoring session → block rendering silently
  if (loading) {
    return null;
  }

  // Not authenticated → redirect to login
  if (!isAuthenticated() || !user) {
    if (onError) {
      onError(new Error("You must be logged in to access this page"));
    }

    return (
      <Navigate
        to="/login"
        replace
        state={{ from: location }}
      />
    );
  }

  // Missing or invalid role → unauthorized
  if (!user.role) {
    toast.error("Access denied: no role assigned.");
    return <Navigate to="/" replace />;
  }

  // User does not have one of the allowed roles
  if (!allowedRoles.includes(user.role)) {
    toast.error("Access denied: insufficient permissions.");
    return <Navigate to="/" replace />;
  }

  // Authorized → allow access
  return children;
}
