import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ loading, isAuthenticated, children }) {
  if (loading) return null; // prevents flash

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
