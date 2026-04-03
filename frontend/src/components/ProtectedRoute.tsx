import { Navigate, useLocation } from "react-router-dom";

export default function ProtectedRoute({ children, roles }) {
  const location = useLocation();

  const token = localStorage.getItem("auth_token");
  const mfa = localStorage.getItem("mfa_verified");
  const role = localStorage.getItem("role");
  const expiry = localStorage.getItem("session_expiry");

  // Session expiration check
  if (expiry && Date.now() > Number(expiry)) {
    localStorage.clear();
    return <Navigate to="/login" replace />;
  }

  if (!token) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (mfa !== "true") {
    return <Navigate to="/mfa/challenge" replace />;
  }

  if (roles && !roles.includes(role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}
