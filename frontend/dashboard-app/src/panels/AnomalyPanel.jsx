// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/panels/AnomalyPanel.jsx

import React, { useEffect, useState, useCallback } from "react";
import { useAuth } from "../services/AuthContext";
import "./anomalyPanel.css";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

/**
 * AnomalyPanel (Modernized)
 *
 * Modern features:
 *   - Uses AuthContext for token + session awareness
 *   - Drift-proof unified refresh function
 *   - Consistent loading/error/empty states
 *   - Operator-grade panel layout
 *   - Auto-refresh every 30s
 *   - Fully aligned with /admin/anomaly routing
 */

export default function AnomalyPanel() {
  const { token, isAuthenticated } = useAuth();

  const [trend, setTrend] = useState([]);
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

      const data = await fetchJSON("/api/anomaly/latest");

      setTrend(data?.trend || []);
    } catch (err) {
      console.error("Anomaly refresh error:", err);
      setError("Failed to refresh anomaly data");
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
      <h1 className="panel-title">Anomaly Detection Panel</h1>

      <button
        className="refresh-button"
        onClick={refreshAll}
        disabled={refreshing}
      >
        {refreshing ? "Refreshing…" : "Refresh"}
      </button>

      {loading && <div className="panel-loading">Loading anomaly data…</div>}
      {error && <div className="panel-error">{error}</div>}

      {!loading && !error && (
        <div className="panel-content">
          <p>
            This is the Anomaly Detection panel. All routing for this panel is
            aligned under <code>/admin/anomaly</code>.
          </p>

          {/* ---------------------------- */}
          {/* Trend Chart                  */}
          {/* ---------------------------- */}
          <div className="panel-section">
            <h2 className="panel-subtitle">Anomaly Trend</h2>

            {trend.length === 0 && (
              <div className="panel-empty">No anomaly data available.</div>
            )}

            {trend.length > 0 && (
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={trend}>
                    <XAxis
                      dataKey="timestamp"
                      tickFormatter={(t) =>
                        new Date(t).toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })
                      }
                    />
                    <YAxis />
                    <Tooltip
                      labelFormatter={(t) =>
                        new Date(t).toLocaleString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                          second: "2-digit",
                        })
                      }
                    />
                    <Line
                      type="monotone"
                      dataKey="count"
                      stroke="#ff4d4d"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
