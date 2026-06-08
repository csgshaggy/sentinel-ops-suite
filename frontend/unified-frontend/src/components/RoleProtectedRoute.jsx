// /src/components/RoleProtectedRoute.jsx
// SentinelOps — Role-Based Route Guard (React Router v6 + Layout-Compatible)

import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { toast } from "./ToastManager.jsx";

export default function RoleProtectedRoute({ allowedRoles = [], onError }) {
  const { user, isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // Wait for session restore
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

  // Missing role → unauthorized
  if (!user.role) {
    toast.error("Access denied: no role assigned.");
    return <Navigate to="/" replace />;
  }

  // User does not have one of the allowed roles
  if (!allowedRoles.includes(user.role)) {
    toast.error("Access denied: insufficient permissions.");
    return <Navigate to="/" replace />;
  }

  // Authorized → allow nested routes to render
  return <Outlet />;
}
