
// /src/pages/SessionMetricsDashboard.jsx

import { useEffect, useState } from "react";
import { getSessionMetrics } from "../../utils/sessionMetrics.js";
import apiClient from "../../api/apiClient.js";

export default function SessionMetricsDashboard() {
  const [metrics, setMetrics] = useState(getSessionMetrics());
  const [ttl, setTtl] = useState(null);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(getSessionMetrics());
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await apiClient.get("/auth/session/ttl");
        setTtl(res?.data?.ttl ?? null);
      } catch {
        setTtl(null);
      }
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const pushEvent = (type) => {
      setEvents((prev) => {
        const next = [
          { ts: new Date().toISOString(), type },
          ...prev,
        ];
        return next.slice(0, 50);
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

  return (
    <div style={{ padding: "20px", fontFamily: "monospace" }}>
      <h2 style={{ marginBottom: "20px" }}>Session Metrics Dashboard</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "20px",
          marginBottom: "30px",
        }}
      >
        <MetricCard title="Heartbeat Count" value={metrics.heartbeatCount} />
        <MetricCard title="Last Heartbeat" value={metrics.lastHeartbeatTs || "—"} />
        <MetricCard
          title="Avg Heartbeat Interval"
          value={
            metrics.avgHeartbeatIntervalMs
              ? Math.round(metrics.avgHeartbeatIntervalMs) + " ms"
              : "—"
          }
        />

        <MetricCard title="Last Activity" value={metrics.lastActivityTs || "—"} />
        <MetricCard title="Restore Count" value={metrics.restoreCount} />
        <MetricCard title="Last Restore" value={metrics.lastRestoreTs || "—"} />

        <MetricCard
          title="Session TTL"
          value={ttl !== null ? ttl + " sec" : "—"}
        />
      </div>

      <h3>Event Stream (last 50)</h3>
      <div
        style={{
          background: "#111",
          color: "#0f0",
          padding: "10px",
          borderRadius: "6px",
          height: "300px",
          overflowY: "auto",
          border: "1px solid #333",
        }}
      >
        {events.length === 0 && (
          <div style={{ opacity: 0.5 }}>No events yet</div>
        )}

        {events.map((evt, i) => (
          <div key={i}>
            <span style={{ color: "#0ff" }}>{evt.type.padEnd(10)}</span>
            <span style={{ opacity: 0.7 }}>{evt.ts}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function MetricCard({ title, value }) {
  return (
    <div
      style={{
        background: "#1a1a1a",
        padding: "14px",
        borderRadius: "6px",
        border: "1px solid #333",
      }}
    >
      <div style={{ opacity: 0.7, marginBottom: "6px" }}>{title}</div>
      <div style={{ fontSize: "18px", color: "#0f0" }}>{value}</div>
    </div>
  );
}
