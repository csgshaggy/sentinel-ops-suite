// /src/hooks/useInactivityLogout.js

import { useEffect, useRef } from "react";
import { toast } from "../components/ToastManager";
import { recordActivity } from "../utils/sessionMetrics.js";
import { logSessionEvent } from "../utils/sessionLogger.js";

/**
 * useInactivityLogout
 * Tracks user inactivity and triggers:
 *  - A warning toast at (timeoutMinutes - warningMinutes)
 *  - onExpire() at timeoutMinutes
 *
 * Supports: disabled=true (used on /login)
 */
export default function useInactivityLogout({
  timeoutMinutes = 15,
  warningMinutes = 3,
  onExpire,
  disabled = false,
}) {
  const lastActivityRef = useRef(Date.now());
  const warningShownRef = useRef(false);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (disabled) {
      if (intervalRef.current) clearInterval(intervalRef.current);
      return;
    }

    const timeoutMs = timeoutMinutes * 60 * 1000;
    const warningMs = timeoutMs - warningMinutes * 60 * 1000;

    const updateActivity = () => {
      recordActivity();
      lastActivityRef.current = Date.now();
      warningShownRef.current = false;
    };

    // Activity events
    const events = ["mousemove", "keydown", "click", "scroll", "touchstart"];
    events.forEach((evt) => window.addEventListener(evt, updateActivity));

    // Check inactivity every second
    intervalRef.current = setInterval(() => {
      const now = Date.now();
      const inactiveFor = now - lastActivityRef.current;

      // Fire warning toast once
      if (inactiveFor >= warningMs && inactiveFor < timeoutMs) {
        if (!warningShownRef.current) {
          warningShownRef.current = true;
          toast.warning("Your session will expire soon due to inactivity.");
        }
      }

      // Auto-logout
      if (inactiveFor >= timeoutMs) {
        clearInterval(intervalRef.current);
        logSessionEvent("inactivity_timeout");
        onExpire?.();
      }
    }, 1000);

    return () => {
      events.forEach((evt) => window.removeEventListener(evt, updateActivity));
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [timeoutMinutes, warningMinutes, onExpire, disabled]);

  return null;
}
