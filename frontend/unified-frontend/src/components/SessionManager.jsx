// /src/components/SessionManager.jsx

import { useEffect, useState, useCallback, useRef } from "react";
import { useLocation } from "react-router-dom";
import { useAuth } from "../features/auth/AuthContext.jsx";
import apiClient from "../api/apiClient.js";
import { toast } from "./ToastManager.jsx";

export default function SessionManager() {
  const { user, logout, restoreSession } = useAuth();
  const location = useLocation();

  const [showWarning, setShowWarning] = useState(false);

  const restoreLock = useRef(false);
  const ttlLock = useRef(false);

  const isPublicRoute =
    location.pathname.startsWith("/login") ||
    location.pathname.startsWith("/mfa");

  const checkTTL = useCallback(async () => {
    if (ttlLock.current) return;
    ttlLock.current = true;

    try {
      const res = await apiClient.get("/auth/session/ttl");

      // ✅ TTL patch: distinguish "missing" from 0
      const ttl = res?.data?.ttl;
      if (ttl === undefined || ttl === null) return;

      // Show warning when <= 60s remaining, otherwise hide
      if (ttl > 0 && ttl <= 60) setShowWarning(true);
      else setShowWarning(false);

      // Expired → logout
      if (ttl <= 0) {
        logout();
      }
    } catch {
      // optional: consider logging
    } finally {
      ttlLock.current = false;
    }
  }, [logout]);

  useEffect(() => {
    if (!user || isPublicRoute) return;

    const interval = setInterval(() => {
      checkTTL();
    }, 30000);

    return () => clearInterval(interval);
  }, [user, isPublicRoute, checkTTL]);

  const stayLoggedIn = async () => {
    if (restoreLock.current) return;
    restoreLock.current = true;

    try {
      await apiClient.get("/auth/heartbeat");
      await restoreSession();

      toast.success("Session extended.");
      setShowWarning(false);
    } catch {
      logout();
    } finally {
      restoreLock.current = false;
    }
  };

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
