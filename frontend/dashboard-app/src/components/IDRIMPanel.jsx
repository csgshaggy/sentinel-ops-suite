// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/components/IDRIMPanel.jsx

import React, { useEffect, useState } from "react";
import "./../styles/panel-shell.css";

export default function IDRIMPanel() {
  const [summary, setSummary] = useState(null);
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        const res1 = await fetch("/api/idrim/summary", {
          method: "GET",
          credentials: "include",
        });

        const res2 = await fetch("/api/idrim/risks", {
          method: "GET",
          credentials: "include",
        });

        if (!res1.ok || !res2.ok) throw new Error("bad response");

        const data1 = await res1.json();
        const data2 = await res2.json();

        if (isMounted) {
          setSummary(data1);
          setRisks(data2.risks || []);
        }
      } catch (err) {
        if (isMounted) {
          setSummary(null);
          setRisks([]);
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
          <h2>IDRIM Panel</h2>
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
        <h2>IDRIM Panel</h2>
      </div>

      <div className="so-panel-body">

        {/* SUMMARY GRID */}
        <div className="so-metric-grid">

          <div className="so-metric-card">
            <h3>Total Risks</h3>
            <p className="so-metric-value">
              {summary?.total_risks ?? "—"}
            </p>
          </div>

          <div className="so-metric-card critical">
            <h3>High Severity</h3>
            <p className="so-metric-value">
              {summary?.high_severity ?? "—"}
            </p>
          </div>

          <div className="so-metric-card">
            <h3>Last Assessment</h3>
            <p className="so-metric-value">
              {summary?.last_assessment ?? "—"}
            </p>
          </div>

        </div>

        {/* RISK REGISTER */}
        <div className="so-events-card">
          <h3 className="so-events-title">Risk Register</h3>

          {risks.length > 0 ? (
            <ul className="so-events-list">
              {risks.map((risk, idx) => (
                <li key={idx} className="so-event-item">
                  <div className="so-event-main">
                    <strong>{risk.name}</strong> — {risk.description}
                  </div>
                  <div className="so-event-meta">
                    Severity: {risk.severity} | Owner: {risk.owner}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="so-panel-empty">No risks recorded.</p>
          )}
        </div>

      </div>
    </div>
  );
}
