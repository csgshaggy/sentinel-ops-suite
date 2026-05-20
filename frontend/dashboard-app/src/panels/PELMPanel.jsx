// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/panels/PELMPanel.jsx

import React, { useEffect, useState, useCallback } from "react";
import { useAuth } from "../services/AuthContext";
import "./pelmPanel.css";

/**
 * PELMPanel (Modernized)
 *
 * Modern features:
 *   - Uses AuthContext for token + session awareness
 *   - Drift-proof unified refresh function
 *   - Consistent loading/error/empty states
 *   - Operator-grade panel layout
 *   - Auto-refresh every 30s
 *   - Fully aligned with /admin/pelm routing
 */

export default function PELMPanel() {
  const { token, isAuthenticated } = useAuth();

  // ----------------------------
  // State Buckets
  // ----------------------------
  const [status, setStatus] = useState(null);
  const [events, setEvents] = useState([]);
  const [engine, setEngine] = useState(null);
  const [paths, setPaths] = useState([]);
  const [audit, setAudit] = useState([]);

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  // ----------------------------
  // Unified Fetch Helper
  // ----------------------------
  const fetchJSON = useCallback(async (url) => {
    const res = await fetch(url, {
      headers: {
        Authorization: token ? `Bearer ${token}` : undefined,
      },
    });

    if (!res.ok) {
      throw new Error(`Failed to fetch ${url}`);
    }

    return res.json();
  }, [token]);

  // ----------------------------
  // Unified Refresh Function
  // ----------------------------
  const refreshAll = useCallback(async () => {
    try {
      setRefreshing(true);
      setError(null);

      const [statusData, eventsData, engineData, pathsData, auditData] =
        await Promise.all([
          fetchJSON("/api/pelm/status"),
          fetchJSON("/api/pelm/events"),
          fetchJSON("/api/pelm/engine"),
          fetchJSON("/api/pelm/paths"),
          fetchJSON("/api/pelm/audit"),
        ]);

      setStatus(statusData);
      setEvents(eventsData);
      setEngine(engineData);
      setPaths(pathsData);
      setAudit(auditData);
    } catch (err) {
      console.error("PELM refresh error:", err);
      setError("Failed to refresh PELM data");
    } finally {
      setRefreshing(false);
      setLoading(false);
    }
  }, [fetchJSON]);

  // ----------------------------
  // Initial Load
  // ----------------------------
  useEffect(() => {
    if (isAuthenticated()) {
      refreshAll();
    }
  }, [isAuthenticated, refreshAll]);

  // ----------------------------
  // Auto-Refresh (every 30 seconds)
  // ----------------------------
  useEffect(() => {
    const interval = setInterval(() => {
      if (isAuthenticated()) refreshAll();
    }, 30000);

    return () => clearInterval(interval);
  }, [isAuthenticated, refreshAll]);

  // ----------------------------
  // Render
  // ----------------------------
  return (
    <div className="panel-container">
      <h1 className="panel-title">PELM Panel</h1>

      <button
        className="refresh-button"
        onClick={refreshAll}
        disabled={refreshing}
      >
        {refreshing ? "Refreshing…" : "Refresh"}
      </button>

      {loading && <div className="panel-loading">Loading PELM data…</div>}
      {error && <div className="panel-error">{error}</div>}

      {!loading && !error && (
        <div className="panel-content">

          {/* ---------------------------- */}
          {/* Status (Raw JSON)            */}
          {/* ---------------------------- */}
          <div className="panel-section">
            <h2 className="panel-subtitle">PELM Status</h2>
            <pre className="panel-json">
              {JSON.stringify(status, null, 2)}
            </pre>
          </div>

          {/* ---------------------------- */}
          {/* Engine Status                */}
          {/* ---------------------------- */}
          <div className="panel-section">
            <h2 className="panel-subtitle">PELM Engine Status</h2>

            {!engine && <div className="panel-empty">No engine data.</div>}

            {engine && (
              <div className="engine-tile">
                <div><strong>Version:</strong> {engine.version}</div>
                <div><strong>Last Run:</strong> {engine.last_run}</div>
                <div><strong>Queue Depth:</strong> {engine.queue_depth}</div>
                <div><strong>Anomalies:</strong> {engine.anomalies}</div>
              </div>
            )}
          </div>

          {/* ---------------------------- */}
          {/* Recent Events                */}
          {/* ---------------------------- */}
          <div className="panel-section">
            <h2 className="panel-subtitle">Recent Lateral Movement Events</h2>

            {events.length === 0 && (
              <div className="panel-empty">No recent events detected.</div>
            )}

            {events.length > 0 && (
              <table className="panel-table">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Source</th>
                    <th>Destination</th>
                    <th>Technique</th>
                  </tr>
                </thead>
                <tbody>
                  {events.map((evt, idx) => (
                    <tr key={idx}>
                      <td>{evt.timestamp}</td>
                      <td>{evt.source}</td>
                      <td>{evt.destination}</td>
                      <td>{evt.technique}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* ---------------------------- */}
          {/* Top Lateral Movement Paths   */}
          {/* ---------------------------- */}
          <div className="panel-section">
            <h2 className="panel-subtitle">Top Lateral Movement Paths</h2>

            {paths.length === 0 && (
              <div className="panel-empty">No lateral movement paths detected.</div>
            )}

            {paths.length > 0 && (
              <ul className="paths-list">
                {paths.map((p, idx) => (
                  <li key={idx} className="paths-item">
                    <strong>{p.source}</strong> → <strong>{p.destination}</strong>
                    <span className="paths-count"> (count: {p.count})</span>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* ---------------------------- */}
          {/* Audit Trail                  */}
          {/* ---------------------------- */}
          <div className="panel-section">
            <h2 className="panel-subtitle">PELM Audit Trail</h2>

            {audit.length === 0 && (
              <div className="panel-empty">No audit entries found.</div>
            )}

            {audit.length > 0 && (
              <pre className="panel-json audit-json">
                {JSON.stringify(audit, null, 2)}
              </pre>
            )}
          </div>

        </div>
      )}
    </div>
  );
}
