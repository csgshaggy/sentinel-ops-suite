// /src/components/SessionDebugOverlay.jsx

import { useEffect, useState } from "react";
import { useAuth } from "../features/auth/AuthContext.jsx";
import { getSessionMetrics } from "../utils/sessionMetrics.js";

const isProd = import.meta.env.PROD;

export default function SessionDebugOverlay() {
  const { user, isAuthenticated } = useAuth();

  const [visible, setVisible] = useState(false);
  const [metrics, setMetrics] = useState(getSessionMetrics());
  const [events, setEvents] = useState([]);

  // ------------------------------------------------------------
  // Toggle overlay: Ctrl + Shift + O
  // ------------------------------------------------------------
  useEffect(() => {
    const handler = (e) => {
      if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "o") {
        setVisible((v) => !v);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  // ------------------------------------------------------------
  // Poll metrics every 2 seconds
  // ------------------------------------------------------------
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(getSessionMetrics());
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  // ------------------------------------------------------------
  // Listen for session events (activity, heartbeat, restore, timeout)
  // ------------------------------------------------------------
  useEffect(() => {
    if (isProd) return;

    const pushEvent = (type) => {
      setEvents((prev) => {
        const next = [
          { ts: new Date().toISOString(), type },
          ...prev,
        ];
        return next.slice(0, 10); // keep last 10
      });
    };

    const handlers = {
      "session-activity": () => pushEvent("activity"),
      "session-heartbeat": () => pushEvent("heartbeat"),
      "session-restore": () => pushEvent("restore"),
      "session-timeout": () => pushEvent("timeout"),
    };

    for (const evt in handlers) {
      window.addEventListener(evt, handlers[evt]);
    }

    return () => {
      for (const evt in handlers) {
        window.removeEventListener(evt, handlers[evt]);
      }
    };
  }, []);

  if (isProd || !visible) return null;

  return (
    <div
      style={{
        position: "fixed",
        top: 20,
        right: 20,
        width: 360,
        background: "rgba(0,0,0,0.88)",
        color: "white",
        padding: 14,
        borderRadius: 8,
        fontFamily: "monospace",
        fontSize: 12,
        zIndex: 99999,
        border: "1px solid #444",
      }}
    >
      <div style={{ fontWeight: "bold", marginBottom: 8, color: "#0f0" }}>
        SESSION DEBUG OVERLAY (Ctrl+Shift+O)
      </div>

      {/* Auth Info */}
      <div>User: {user ? user.username : "None"}</div>
      <div>Authenticated: {isAuthenticated() ? "Yes" : "No"}</div>

      <hr style={{ margin: "8px 0", opacity: 0.3 }} />

      {/* Metrics */}
      <div>Heartbeat Count: {metrics.heartbeatCount}</div>
      <div>Last Heartbeat: {metrics.lastHeartbeatTs || "—"}</div>
      <div>
        Avg Heartbeat Interval:{" "}
        {metrics.avgHeartbeatIntervalMs
          ? Math.round(metrics.avgHeartbeatIntervalMs) + " ms"
          : "—"}
      </div>

      <div>Last Activity: {metrics.lastActivityTs || "—"}</div>

      <div>Restore Count: {metrics.restoreCount}</div>
      <div>Last Restore: {metrics.lastRestoreTs || "—"}</div>

      <hr style={{ margin: "8px 0", opacity: 0.3 }} />

      {/* Event Log */}
      <div style={{ fontWeight: "bold", marginBottom: 4 }}>Recent Events:</div>

      <div
        style={{
          maxHeight: 160,
          overflowY: "auto",
          background: "rgba(255,255,255,0.05)",
          padding: 6,
          borderRadius: 4,
          border: "1px solid #333",
        }}
      >
        {events.length === 0 && <div style={{ opacity: 0.5 }}>No events yet</div>}

        {events.map((evt, i) => (
          <div key={i} style={{ marginBottom: 2 }}>
            <span style={{ color: "#0f0" }}>{evt.type.padEnd(10)}</span>
            <span style={{ opacity: 0.7 }}>{evt.ts}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
