// /src/components/SessionDebugOverlay.jsx

import { useEffect, useState } from "react";
import { useAuth } from "../features/auth/AuthContext.jsx";

export default function SessionDebugOverlay() {
  const { user, isAuthenticated } = useAuth();

  const [visible, setVisible] = useState(false);
  const [lastHeartbeat, setLastHeartbeat] = useState(null);
  const [lastActivity, setLastActivity] = useState(null);
  const [lastRestore, setLastRestore] = useState(null);

  // Listen for operator toggle: Ctrl + Shift + O
  useEffect(() => {
    const handler = (e) => {
      if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "o") {
        setVisible((v) => !v);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  // Listen for custom events emitted by hooks
  useEffect(() => {
    const heartbeatListener = () => setLastHeartbeat(new Date().toISOString());
    const activityListener = () => setLastActivity(new Date().toISOString());
    const restoreListener = () => setLastRestore(new Date().toISOString());

    window.addEventListener("session-heartbeat", heartbeatListener);
    window.addEventListener("session-activity", activityListener);
    window.addEventListener("session-restore", restoreListener);

    return () => {
      window.removeEventListener("session-heartbeat", heartbeatListener);
      window.removeEventListener("session-activity", activityListener);
      window.removeEventListener("session-restore", restoreListener);
    };
  }, []);

  if (!visible) return null;

  return (
    <div
      style={{
        position: "fixed",
        bottom: 20,
        right: 20,
        background: "rgba(0,0,0,0.85)",
        padding: "16px",
        borderRadius: "8px",
        color: "white",
        fontSize: "13px",
        zIndex: 99999,
        width: "320px",
        fontFamily: "monospace",
      }}
    >
      <div style={{ marginBottom: "8px", fontWeight: "bold" }}>
        SESSION DEBUG OVERLAY
      </div>

      <div>User: {user ? user.username : "None"}</div>
      <div>Authenticated: {isAuthenticated() ? "Yes" : "No"}</div>

      <hr style={{ margin: "8px 0", opacity: 0.3 }} />

      <div>Last Heartbeat: {lastHeartbeat || "—"}</div>
      <div>Last Activity: {lastActivity || "—"}</div>
      <div>Last Restore: {lastRestore || "—"}</div>

      <hr style={{ margin: "8px 0", opacity: 0.3 }} />

      <div style={{ opacity: 0.6 }}>
        Toggle: Ctrl + Shift + O
      </div>
    </div>
  );
}
