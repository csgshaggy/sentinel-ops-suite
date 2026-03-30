// =====================================================================
// SSRF Command Console — Admin Dashboard Metrics Page
// =====================================================================

import { useEffect, useState } from "react";
import { fetchMetrics } from "../../api/admin";
import MetricCard from "../../components/MetricCard";

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchMetrics();
        setMetrics(data);
      } catch {
        setError("Failed to load metrics");
      }
    }
    load();
  }, []);

  if (error) {
    return (
      <div className="panel" style={{ margin: "2rem" }}>
        <div className="error">{error}</div>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="panel" style={{ margin: "2rem" }}>
        Loading...
      </div>
    );
  }

  return (
    <div style={{ margin: "2rem" }}>
      <h2>Admin Dashboard</h2>

      <div
        style={{
          display: "flex",
          gap: "1rem",
          marginTop: "1rem",
          flexWrap: "wrap",
        }}
      >
        <MetricCard label="Total Users" value={metrics.total_users} />
        <MetricCard label="Active Users" value={metrics.active_users} />
        <MetricCard label="Inactive Users" value={metrics.inactive_users} />
        <MetricCard label="Logins (7 days)" value={metrics.recent_logins} />
      </div>

      <div className="panel" style={{ marginTop: "2rem" }}>
        <h3>Role Distribution</h3>
        <ul style={{ marginTop: "0.5rem" }}>
          {Object.entries(metrics.roles).map(([role, count]) => (
            <li key={role}>
              <strong>{role}</strong>: {count}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
