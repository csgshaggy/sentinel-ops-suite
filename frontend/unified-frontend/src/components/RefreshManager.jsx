// /src/components/RefreshManager.jsx
// SentinelOps — Background Sliding Session Refresh

import { useEffect } from "react";
import client from "../api/apiClient.js";

export default function RefreshManager() {
  useEffect(() => {
    let active = true;

    const loop = async () => {
      while (active) {
        try {
          await client.get("/auth/refresh");
        } catch {
          // AuthContext handles 401
        }
        await new Promise((r) => setTimeout(r, 60_000));
      }
    };

    loop();
    return () => {
      active = false;
    };
  }, []);

  return null;
}
