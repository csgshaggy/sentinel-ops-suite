// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/panels/IDRIMPanel.jsx

import React, { useEffect, useState, useCallback } from "react";
import { useAuth } from "../services/AuthContext";
import "./idrimPanel.css";

/**
 * IDRIMPanel (Modernized)
 *
 * Modern features:
 *   - Uses AuthContext for token + session awareness
 *   - Drift-proof unified refresh function
 *   - Consistent loading/error/empty states
 *   - Operator-grade panel layout
 *   - Auto-refresh every 30s
 *   - Fully aligned with /admin/idrim routing
 */

export default function IDRIMPanel() {
  const { token, isAuthenticated } = useAuth();

  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  // ----------------------------
  // Unified Fetch Helper
  // ----------------------------
  const fetchJSON = useCallback(
    async (url) => {
      const res = await fetch(url, {
        headers: {
          Authorization: token ? `Bearer ${token}` : undefined,
        },
      });

      if (!res.ok) {
        throw new Error(`Failed to fetch ${url}`);
      }

      return res.json();
    },
    [token]
  );

  // ----------------------------
  // Unified Refresh Function
  // ----------------------------
  const refreshAll = useCallback(async () => {
    try {
      setRefreshing(true);
      setError(null);

      const data = await fetchJSON("/api/idrim/summary");
      setSummary(data);
    } catch (err) {
      console.error("IDRIM refresh error:", err);
      setError("Failed to refresh IDRIM data");
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
      <h1 className="panel-title">IDRIM Panel</h1>

      <button
        className="refresh-button"
        onClick={refreshAll}
        disabled={refreshing}
      >
        {refreshing ? "Refreshing…" : "Refresh"}
      </button>

      {loading && <div className="panel-loading">Loading IDRIM data…</div>}
      {error && <div className="panel-error">{error}</div>}

      {!loading && !error && (
        <div className="panel-content">
          <p>
            This is the IDRIM (Identity Risk & Misconfiguration) panel.
            All routing for this panel is aligned under <code>/admin/idrim</code>.
          </p>

          {/* ---------------------------- */}
          {/* Summary JSON                 */}
          {/* ---------------------------- */}
          <div className="panel-section">
            <h2 className="panel-subtitle">IDRIM Summary</h2>

            {!summary && (
              <div className="panel-empty">No IDRIM summary available.</div>
            )}

            {summary && (
              <pre className="panel-json">
                {JSON.stringify(summary, null, 2)}
              </pre>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
