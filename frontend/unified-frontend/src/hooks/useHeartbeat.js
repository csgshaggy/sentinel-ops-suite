// /src/hooks/useHeartbeat.js

import { useEffect } from "react";
import apiClient from "../api/apiClient.js";

import { recordHeartbeat } from "../utils/sessionMetrics.js";
import { logSessionEvent } from "../utils/sessionLogger.js";

/**
 * useHeartbeat
 * Sends a silent heartbeat every 5 minutes to refresh the session TTL.
 * Now supports: disabled=true (used on /login)
 */
export default function useHeartbeat(isAuthenticated, disabled = false) {
  useEffect(() => {
    if (!isAuthenticated || disabled) return;   // <-- NEW: disable on login

    const interval = setInterval(async () => {
      try {
        // Silent session refresh — backend extends TTL
        await apiClient.get("/auth/heartbeat");

        // --- Operator‑mode instrumentation ---
        recordHeartbeat();
        logSessionEvent("heartbeat_refresh");
        window.dispatchEvent(new Event("session-heartbeat"));

      } catch {
        // Ignore — inactivity/logout logic will handle expiration
      }
    }, 5 * 60 * 1000); // every 5 minutes

    return () => clearInterval(interval);
  }, [isAuthenticated, disabled]);
}
