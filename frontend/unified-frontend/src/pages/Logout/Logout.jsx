// /src/pages/Logout/Logout.jsx
// SentinelOps — Logout Page

import { useEffect } from "react";
import { useAuth } from "../../features/auth/AuthContext.jsx";

export default function Logout() {
  const { logout } = useAuth();

  useEffect(() => {
    logout();
  }, [logout]);

  return null;
}
