// /src/pages/Dashboard.jsx
import React, { useEffect, useState } from "react";
import { useAuth } from "../features/auth/AuthContext.jsx";
import "./Dashboard.css";

export default function Dashboard() {
  const { user } = useAuth();

  const [backendStatus, setBackendStatus] = useState("checking");
  const [backendLatency, setBackendLatency] = useState(null);

  async function checkBackend() {
    const start = performance.now();

    try {
      const res = await fetch("/api/users/me", {
        method: "GET",
        credentials: "include",
      });

      const end = performance.now();
      setBackendLatency(Math.round(end - start));

      if (res.status === 401 || res.status === 200) {
        setBackendStatus("online");
      } else {
        setBackendStatus("degraded");
      }
    } catch {
      setBackendStatus("offline");
    }
  }

  useEffect(() => {
    checkBackend();
  }, []);

  return (
    <div className="dashboard-page fade-in">
      <h1 className="dashboard-title">SentinelOps Operational Dashboard</h1>

      {/* Backend Status */}
      <section className="dashboard-section">
        <h2 className="dashboard-section-title">Backend Status</h2>

        <div className="dashboard-metric-row">
          <div className="dashboard-metric-card">
            <div className="metric-label">Status</div>
            <div
              className={`metric-value ${
                backendStatus === "online"
                  ? "metric-ok"
                  : backendStatus === "offline"
                  ? "metric-bad"
                  : "metric-warn"
              }`}
            >
              {backendStatus}
            </div>
          </div>

          <div className="dashboard-metric-card">
            <div className="metric-label">Latency</div>
            <div className="metric-value">
              {backendLatency !== null ? `${backendLatency} ms` : "—"}
            </div>
          </div>
        </div>
      </section>

      {/* User Identity */}
      <section className="dashboard-section">
        <h2 className="dashboard-section-title">User Identity</h2>

        {user ? (
          <div className="identity-grid">
            <div className="identity-item">
              <span className="identity-label">Username:</span>
              <span className="identity-value">{user.username}</span>
            </div>

            <div className="identity-item">
              <span className="identity-label">Email:</span>
              <span className="identity-value">{user.email}</span>
            </div>

            <div className="identity-item">
              <span className="identity-label">Role:</span>
              <span className="identity-value">{user.role}</span>
            </div>

            <div className="identity-item">
              <span className="identity-label">MFA Enabled:</span>
              <span className="identity-value">
                {user.mfa_enabled ? "Yes" : "No"}
              </span>
            </div>
          </div>
        ) : (
          <div className="dashboard-loading">Loading user profile…</div>
        )}
      </section>

      {/* Remaining sections unchanged */}
    </div>
  );
}
