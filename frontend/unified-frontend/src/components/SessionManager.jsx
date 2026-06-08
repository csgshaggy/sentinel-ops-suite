// /src/components/SessionManager.jsx
// SentinelOps — Session Manager (Final, Fetch‑Aligned, Deterministic)

import { useEffect, useState, useCallback, useRef } from "react";
import { useLocation } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import apiClient from "../api/apiClient.js";
import { toast } from "./ToastManager.jsx";

export default function SessionManager() {
  const { user, logout, refreshUser } = useAuth();
  const location = useLocation();

  const [showWarning, setShowWarning] = useState(false);

  const ttlLock = useRef(false);
  const restoreLock = useRef(false);

  // Public routes should NOT trigger TTL or heartbeat
  const isPublicRoute =
    location.pathname.startsWith("/login") ||
    location.pathname.startsWith("/mfa");

  // ------------------------------------------------------------
  // TTL CHECK — fetch‑aligned (no try/catch, no err.response)
  // ------------------------------------------------------------
  const checkTTL = useCallback(async () => {
    if (ttlLock.current) return;
    ttlLock.current = true;

    const res = await apiClient.get("/auth/session/ttl");

    if (!res.ok) {
      // 401 = not logged in → ignore silently
      if (res.status !== 401) {
        console.error("TTL check error:", res);
      }
      ttlLock.current = false;
      return;
    }

    const ttl = res.data?.ttl;

    if (ttl === undefined || ttl === null) {
      ttlLock.current = false;
      return;
    }

    if (ttl > 0 && ttl <= 60) setShowWarning(true);
    else setShowWarning(false);

    if (ttl <= 0) logout();

    ttlLock.current = false;
  }, [logout]);

  // ------------------------------------------------------------
  // TTL polling — disabled on public routes
  // ------------------------------------------------------------
  useEffect(() => {
    if (!user || isPublicRoute) return;

    const interval = setInterval(() => {
      checkTTL();
    }, 30000);

    return () => clearInterval(interval);
  }, [user, isPublicRoute, checkTTL]);

  // ------------------------------------------------------------
  // Stay Logged In — heartbeat + refreshUser
  // ------------------------------------------------------------
  const stayLoggedIn = async () => {
    if (restoreLock.current) return;
    restoreLock.current = true;

    const res = await apiClient.get("/auth/heartbeat");

    if (!res.ok) {
      if (res.status !== 401) {
        console.error("Heartbeat error:", res);
      }
      logout();
      restoreLock.current = false;
      return;
    }

    await refreshUser();
    toast.success("Session extended.");
    setShowWarning(false);

    restoreLock.current = false;
  };

  // ------------------------------------------------------------
  // Render warning modal (never on public routes)
  // ------------------------------------------------------------
  if (!showWarning || isPublicRoute) return null;

  return (
    <div className="session-warning-modal">
      <div className="modal-content">
        <h3>Session Expiring Soon</h3>
        <p>Your session is about to expire.</p>

        <div className="modal-actions">
          <button onClick={stayLoggedIn} className="btn-primary">
            Stay Logged In
          </button>
          <button onClick={logout} className="btn-secondary">
            Log Out Now
          </button>
        </div>
      </div>
    </div>
  );
}

