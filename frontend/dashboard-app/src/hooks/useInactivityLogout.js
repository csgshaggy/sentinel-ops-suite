// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/hooks/useInactivityLogout.js

import { useEffect, useRef } from "react";

/**
 * useInactivityLogout
 *
 * Tracks user inactivity and triggers:
 *  - onWarning() at T‑1 minute
 *  - onExpire() at T minutes
 *
 * Guarantees:
 *  - No double warnings
 *  - No double expirations
 *  - No stale closures
 *  - No interval duplication
 *  - No listener duplication
 */
export default function useInactivityLogout({
  timeoutMinutes = 15,
  onWarning = () => {},
  onExpire = () => {}
}) {
  const lastActivityRef = useRef(Date.now());
  const warningShownRef = useRef(false);
  const intervalRef = useRef(null);

  // Stable callback refs to avoid stale closures
  const onWarningRef = useRef(onWarning);
  const onExpireRef = useRef(onExpire);

  useEffect(() => {
    onWarningRef.current = onWarning;
  }, [onWarning]);

  useEffect(() => {
    onExpireRef.current = onExpire;
  }, [onExpire]);

  useEffect(() => {
    const timeoutMs = timeoutMinutes * 60 * 1000;      // 15 minutes
    const warningMs = timeoutMs - 60 * 1000;           // 14 minutes

    // Reset activity timestamp
    const updateActivity = () => {
      lastActivityRef.current = Date.now();
      warningShownRef.current = false; // reset warning state
    };

    // Attach listeners
    const events = ["mousemove", "keydown", "click", "scroll"];
    events.forEach((evt) => window.addEventListener(evt, updateActivity));

    // Check inactivity every second
    intervalRef.current = setInterval(() => {
      const now = Date.now();
      const inactiveFor = now - lastActivityRef.current;

      // 14‑minute warning
      if (inactiveFor >= warningMs && inactiveFor < timeoutMs) {
        if (!warningShownRef.current) {
          warningShownRef.current = true;
          onWarningRef.current();
        }
      }

      // 15‑minute expiration
      if (inactiveFor >= timeoutMs) {
        clearInterval(intervalRef.current);
        onExpireRef.current();
      }
    }, 1000);

    return () => {
      events.forEach((evt) => window.removeEventListener(evt, updateActivity));
      clearInterval(intervalRef.current);
    };
  }, [timeoutMinutes]);
}
