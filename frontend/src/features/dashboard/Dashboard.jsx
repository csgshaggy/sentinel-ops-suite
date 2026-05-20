// File: src/features/dashboard/Dashboard.jsx

import { useEffect, useState } from "react";
import api from "../../api/client";
import "./dashboard.css";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/dashboard/summary")
      .then((res) => setSummary(res.data))
      .catch(() => setError("Failed to load dashboard summary"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="dashboard-loading">Loading dashboard…</div>;
  if (error) return <div className="dashboard-error">{error}</div>;

  return (
    <div className="dashboard-container">
      <h1>SentinelOps Dashboard</h1>

      <div className="dashboard-grid">
        {summary?.tiles?.map((tile) => (
          <div key={tile.id} className="dashboard-tile">
            <h3>{tile.title}</h3>
            <p>{tile.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
