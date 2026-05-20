// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/components/GitHealthPanel.jsx

import React, { useEffect, useState } from "react";
import "./../styles/panel-shell.css";

export default function GitHealthPanel() {
  const [summary, setSummary] = useState(null);
  const [commits, setCommits] = useState([]);
  const [branches, setBranches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        const res1 = await fetch("/api/git/summary", {
          method: "GET",
          credentials: "include",
        });

        const res2 = await fetch("/api/git/commits", {
          method: "GET",
          credentials: "include",
        });

        const res3 = await fetch("/api/git/branches", {
          method: "GET",
          credentials: "include",
        });

        if (!res1.ok || !res2.ok || !res3.ok) throw new Error("bad response");

        const data1 = await res1.json();
        const data2 = await res2.json();
        const data3 = await res3.json();

        if (isMounted) {
          setSummary(data1);
          setCommits(data2.commits || []);
          setBranches(data3.branches || []);
        }
      } catch (err) {
        if (isMounted) {
          setSummary(null);
          setCommits([]);
          setBranches([]);
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
          <h2>Git Health</h2>
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
        <h2>Git Health</h2>
      </div>

      <div className="so-panel-body">

        {/* SUMMARY GRID */}
        <div className="so-metric-grid">

          <div className="so-metric-card">
            <h3>Active Branches</h3>
            <p className="so-metric-value">
              {summary?.active_branches ?? "—"}
            </p>
          </div>

          <div className="so-metric-card critical">
            <h3>Stale Branches</h3>
            <p className="so-metric-value">
              {summary?.stale_branches ?? "—"}
            </p>
          </div>

          <div className="so-metric-card">
            <h3>Last Commit</h3>
            <p className="so-metric-value">
              {summary?.last_commit ?? "—"}
            </p>
          </div>

        </div>

        {/* RECENT COMMITS */}
        <div className="so-events-card">
          <h3 className="so-events-title">Recent Commits</h3>

          {commits.length > 0 ? (
            <ul className="so-events-list">
              {commits.map((c, idx) => (
                <li key={idx} className="so-event-item">
                  <div className="so-event-main">
                    <strong>{c.message}</strong>
                  </div>
                  <div className="so-event-meta">
                    {c.author} — {c.timestamp}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="so-panel-empty">No recent commits.</p>
          )}
        </div>

        {/* BRANCH LIST */}
        <div className="so-events-card">
          <h3 className="so-events-title">Branches</h3>

          {branches.length > 0 ? (
            <ul className="so-events-list">
              {branches.map((b, idx) => (
                <li key={idx} className="so-event-item">
                  <div className="so-event-main">
                    <strong>{b.name}</strong>
                  </div>
                  <div className="so-event-meta">
                    Last commit: {b.last_commit}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="so-panel-empty">No branches found.</p>
          )}
        </div>

      </div>
    </div>
  );
}
