// /src/components/ProtectedRoute.jsx
// SentinelOps — Protected Route (React Router v6 + Layout-Compatible)

import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { isAuthRoute } from "../utils/isAuthRoute.js";

export default function ProtectedRoute() {
  const { user, loading } = useAuth();
  const location = useLocation();

  const isPublic = isAuthRoute(location.pathname);

  // Public routes bypass protection
  if (isPublic) {
    return <Outlet />;
  }

  // Wait for session restore
  if (loading) {
    return null;
  }

  // Not authenticated → redirect to login
  if (!user) {
    const redirectTo = encodeURIComponent(location.pathname);
    return <Navigate to={`/login?redirectTo=${redirectTo}`} replace />;
  }

  // Authenticated → allow nested routes to render
  return <Outlet />;
}
