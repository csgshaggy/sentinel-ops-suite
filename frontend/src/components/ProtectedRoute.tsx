// frontend/src/components/ProtectedRoute.tsx
// SentinelOps — Session‑Hydrating Protected Route

import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/client"; // your axios instance with cookies enabled

export default function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { user, login, logout } = useAuth();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    async function hydrate() {
      try {
        // Hit the backend session endpoint
        const res = await api.get("/api/users/me");

        // If successful → hydrate context
        if (res?.data) {
          login(res.data);
          setChecking(false);
          return;
        }

        // If no data, treat as unauthenticated
        logout();
        setChecking(false);
      } catch (err: any) {
        // 401 → session expired or not logged in
        if (err?.response?.status === 401) {
          logout();
          setChecking(false);
          return;
        }

        // Any other error → fail closed
        console.error("ProtectedRoute hydration error:", err);
        logout();
        setChecking(false);
      }
    }

    hydrate();
  }, []);

  if (checking) {
    return (
      <div style={{ padding: "2rem", textAlign: "center", color: "#fff" }}>
        Checking session…
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/admin/login" replace />;
  }

  return children;
}
