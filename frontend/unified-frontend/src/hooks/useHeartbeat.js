// /src/hooks/useHeartbeat.js

import { useEffect } from "react";
import apiClient from "../api/apiClient.js";

import { recordHeartbeat } from "../utils/sessionMetrics.js";
import { logSessionEvent } from "../utils/sessionLogger.js";

/**
 * useHeartbeat
 * Silent liveness check every 5 minutes.
 * Backend no longer extends TTL — sliding expiration happens server-side.
 * Supports: disabled=true (used on /login)
 */
export default function useHeartbeat(isAuthenticated, disabled = false) {
  useEffect(() => {
    if (!isAuthenticated || disabled) return;

    const interval = setInterval(async () => {
      try {
        // Heartbeat: backend returns { active: boolean }
        const res = await apiClient.get("/api/auth/heartbeat");

        // --- Operator‑mode instrumentation ---
        recordHeartbeat();
        logSessionEvent("heartbeat_check");
        window.dispatchEvent(new Event("session-heartbeat"));

        // If backend reports inactive, frontend will handle logout elsewhere
        if (!res?.data?.active) {
          logSessionEvent("heartbeat_inactive");
        }

      } catch {
        // Ignore — session middleware + restore logic handle expiration
        logSessionEvent("heartbeat_error");
      }
    }, 5 * 60 * 1000); // every 5 minutes

    return () => clearInterval(interval);
  }, [isAuthenticated, disabled]);
}
