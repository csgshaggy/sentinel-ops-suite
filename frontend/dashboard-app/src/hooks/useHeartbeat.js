// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/hooks/useHeartbeat.js

import { useEffect } from "react";

/**
 * useHeartbeat
 * Sends a keep‑alive ping every 5 minutes *only* when the user is authenticated.
 *
 * @param {Function} isAuthenticated - A function that returns true/false.
 */
export default function useHeartbeat(isAuthenticated) {
  useEffect(() => {
    // Guard: ensure we were passed a function
    if (typeof isAuthenticated !== "function") {
      console.warn("useHeartbeat expected a function but received:", isAuthenticated);
      return;
    }

    // If user is not authenticated, do not start heartbeat
    if (!isAuthenticated()) return;

    const interval = setInterval(() => {
      // Only ping if still authenticated at the moment of execution
      if (!isAuthenticated()) return;

      fetch("/api/heartbeat", {
        method: "GET",
        credentials: "include",
      }).catch(() => {
        // Silent fail — inactivity/logout logic handles session expiration
      });
    }, 5 * 60 * 1000); // every 5 minutes

    return () => clearInterval(interval);
  }, [isAuthenticated]);
}
