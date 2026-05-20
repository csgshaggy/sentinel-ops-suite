// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/components/RepoHealthPanel.jsx

import React, { useEffect, useState } from "react";
import "./../styles/panel-shell.css";

export default function RepoHealthPanel() {
  const [summary, setSummary] = useState(null);
  const [issues, setIssues] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        const res1 = await fetch("/api/repo/summary", {
          method: "GET",
          credentials: "include",
        });

        const res2 = await fetch("/api/repo/issues", {
          method: "GET",
          credentials: "include",
        });

        const res3 = await fetch("/api/repo/metrics", {
          method: "GET",
          credentials: "include",
        });

        if (!res1.ok || !res2.ok || !res3.ok) throw new Error("bad response");

        const data1 = await res1.json();
        const data2 = await res2.json();
        const data3 = await res3.json();

        if (isMounted) {
          setSummary(data1);
          setIssues(data2.issues || []);
          setMetrics(data3);
        }
      } catch (err) {
        if (isMounted) {
          setSummary(null);
          setIssues([]);
          setMetrics(null);
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    fetchData();
    return () => { isMounted = false; };
  }, []);

  if (loading) {
    return (
      <div className="so-panel">
        <div className="so-panel-header">
          <h2>Repo Health</h2>
        </div>
        <div className="so-panel-body">
          <p className="so-panel-loading">Loading…</p>
        </div>
      </div>
    );
  }

  return (
    <div className="so-panel">

      {/* PANEL HEADER */}
      <div className="so-panel-header">
        <h2>Repo Health</h2>
      </div>

      <div className="so-panel-body">

        {/* SUMMARY GRID */}
        <div className="so-metric-grid">

          <div className="so-metric-card">
            <h3>Open Issues</h3>
            <p className="so-metric-value">
              {summary?.open_issues ?? "—"}
            </p>
          </div>

          <div className="so-metric-card critical">
            <h3>Critical Issues</h3>
            <p className="so-metric-value">
              {summary?.critical_issues ?? "—"}
            </p>
          </div>

          <div className="so-metric-card">
            <h3>Last Sync</h3>
            <p className="so-metric-value">
              {summary?.last_sync ?? "—"}
            </p>
          </div>

        </div>

        {/* METRICS */}
        <div className="so-events-card">
          <h3 className="so-events-title">Repository Metrics</h3>

          {metrics ? (
            <ul className="so-events-list">
              <li className="so-event-item">
                <div className="so-event-main">
                  <strong>Commits (30d):</strong> {metrics.commits_30d}
                </div>
              </li>

              <li className="so-event-item">
                <div className="so-event-main">
                  <strong>Contributors:</strong> {metrics.contributors}
                </div>
              </li>

              <li className="so-event-item">
                <div className="so-event-main">
                  <strong>Stale Branches:</strong> {metrics.stale_branches}
                </div>
              </li>
            </ul>
          ) : (
            <p className="so-panel-empty">No metrics available.</p>
          )}
        </div>

        {/* ISSUES LIST */}
        <div className="so-events-card">
          <h3 className="so-events-title">Issue List</h3>

          {issues.length > 0 ? (
            <ul className="so-events-list">
              {issues.map((issue, idx) => (
                <li key={idx} className="so-event-item">
                  <div className="so-event-main">
                    <strong>{issue.title}</strong>
                  </div>
                  <div className="so-event-meta">
                    #{issue.id} — {issue.status} — {issue.created_at}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="so-panel-empty">No issues found.</p>
          )}
        </div>

      </div>
    </div>
  );
}
