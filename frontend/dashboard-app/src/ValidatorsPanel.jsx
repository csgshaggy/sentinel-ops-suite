// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/components/ValidatorsPanel.jsx

import React, { useEffect, useState } from "react";
import "./../styles/panel-shell.css";

export default function ValidatorsPanel() {
  const [summary, setSummary] = useState(null);
  const [validators, setValidators] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        // Placeholder endpoints — adjust to your backend
        const res1 = await fetch("/api/validators/summary", {
          method: "GET",
          credentials: "include",
        });

        const res2 = await fetch("/api/validators/list", {
          method: "GET",
          credentials: "include",
        });

        if (!res1.ok || !res2.ok) throw new Error("bad response");

        const data1 = await res1.json();
        const data2 = await res2.json();

        if (isMounted) {
          setSummary(data1);
          setValidators(data2.validators || []);
        }
      } catch (err) {
        if (isMounted) {
          setSummary(null);
          setValidators([]);
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
          <h2>Validators</h2>
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
        <h2>Validators</h2>
      </div>

      <div className="so-panel-body">

        {/* SUMMARY GRID */}
        <div className="so-metric-grid">

          <div className="so-metric-card">
            <h3>Total Validators</h3>
            <p className="so-metric-value">
              {summary?.total ?? "—"}
            </p>
          </div>

          <div className="so-metric-card critical">
            <h3>Failed</h3>
            <p className="so-metric-value">
              {summary?.failed ?? "—"}
            </p>
          </div>

          <div className="so-metric-card">
            <h3>Last Run</h3>
            <p className="so-metric-value">
              {summary?.last_run ?? "—"}
            </p>
          </div>

        </div>

        {/* VALIDATOR LIST */}
        <div className="so-events-card">
          <h3 className="so-events-title">Validator Results</h3>

          {validators.length > 0 ? (
            <ul className="so-events-list">
              {validators.map((v, idx) => (
                <li key={idx} className="so-event-item">
                  <div className="so-event-main">
                    <strong>{v.name}</strong> — {v.status}
                  </div>
                  <div className="so-event-meta">
                    {v.timestamp}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="so-panel-empty">No validator results available.</p>
          )}
        </div>

      </div>
    </div>
  );
}
