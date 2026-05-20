// /src/components/ProtectedRoute.jsx

import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { isAuthRoute } from "../utils/isAuthRoute.js";

/**
 * ProtectedRoute
 * - Blocks access unless user is authenticated
 * - Skips protection for public routes (login, mfa)
 * - Prevents redirect loops
 */
export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  const isPublic = isAuthRoute(location.pathname);

  // Public routes should NEVER be protected
  if (isPublic) {
    return children;
  }

  // Still restoring session → don't redirect yet
  if (loading) {
    return null;
  }

  // Not authenticated → redirect to login
  if (!user) {
    return (
      <Navigate
        to={`/login?redirectTo=${encodeURIComponent(location.pathname)}`}
        replace
      />
    );
  }

  // Authenticated → render wrapped tree
  return children;
}
