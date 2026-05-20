import { useEffect, useState } from "react";
import { useSessionExpire } from "../components/modals/SessionExpireManager.jsx";

const HEARTBEAT_INTERVAL_MS = 60_000; // 60 seconds

export function useSession() {
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Access modal controls
  const { showModal } = useSessionExpire();

  // Initial session check
  useEffect(() => {
    async function checkSession() {
      try {
        const res = await fetch("/api/auth/session", {
          credentials: "include",
        });

        if (res.ok) {
          const data = await res.json();

          const active = data.active === true;
          setIsAuthenticated(active);

          // Backend says session is expired
          if (!active) {
            showModal();
          }
        } else {
          // Non-200 response = session invalid
          setIsAuthenticated(false);
          showModal();
        }
      } catch (err) {
        // Network or server error = treat as expired
        setIsAuthenticated(false);
        showModal();
      } finally {
        setLoading(false);
      }
    }

    checkSession();
  }, [showModal]);

  // Heartbeat pings
  useEffect(() => {
    if (!isAuthenticated) return;

    let intervalId;

    async function sendHeartbeat() {
      try {
        const res = await fetch("/api/auth/heartbeat", {
          method: "POST",
          credentials: "include",
        });

        // If backend rejects heartbeat, session is dead
        if (res.status === 401 || res.status === 419) {
          showModal();
        }
      } catch (err) {
        // Network failure — do not flip auth immediately
        // Session check logic will handle it
      }
    }

    intervalId = setInterval(sendHeartbeat, HEARTBEAT_INTERVAL_MS);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isAuthenticated, showModal]);

  return { loading, isAuthenticated };
}
