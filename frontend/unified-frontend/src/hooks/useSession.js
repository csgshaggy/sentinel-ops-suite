// /src/hooks/useSession.js
// SentinelOps — Session Heartbeat Hook

import { useEffect, useState, useCallback } from "react";
import client from "../api/apiClient.js";

export default function useSession(intervalMs = 60_000) {
  const [alive, setAlive] = useState(null);
  const [lastCheck, setLastCheck] = useState(Date.now());

  const check = useCallback(async () => {
    try {
      // FIXED: send session cookie with request
      const res = await client.get("/auth/profile", {
        withCredentials: true,
      });

      setAlive(res.status === 200);
    } catch {
      setAlive(false);
    } finally {
      setLastCheck(Date.now());
    }
  }, []);

  useEffect(() => {
    let active = true;

    const loop = async () => {
      while (active) {
        await check();
        await new Promise((r) => setTimeout(r, intervalMs));
      }
    };

    loop();
    return () => {
      active = false;
    };
  }, [check, intervalMs]);

  return { alive, lastCheck, check };
}
