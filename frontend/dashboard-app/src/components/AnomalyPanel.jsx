// /home/ubuntu/sentinel-ops-suite/frontend/dashboard-app/src/components/AnomalyPanel.jsx

import React, { useEffect, useState } from "react";
import "./../styles/panel-shell.css";

export default function AnomalyPanel() {
  const [summary, setSummary] = useState(null);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        const res1 = await fetch("/api/anomaly/summary", {
          method: "GET",
          credentials: "include",
        });

        const res2 = await fetch("/api/anomaly/events", {
          method: "GET",
          credentials: "include",
        });

        if (!res1.ok || !res2.ok) throw new Error("bad response");

        const data1 = await res1.json();
        const data2 = await res2.json();

        if (isMounted) {
          setSummary(data1);
          setEvents(data2.events || []);
        }
      } catch (err) {
        if (isMounted) {
          setSummary(null);
          setEvents([]);
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
          <h2>Anomaly Detection</h2>
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
        <h2>Anomaly Detection</h2>
      </div>

      <div className="so-panel-body">

        {/* SUMMARY GRID */}
        <div className="so-metric-grid">

          <div className="so-metric-card">
            <h3>Total Anomalies</h3>
            <p className="so-metric-value">
              {summary?.total_anomalies ?? "—"}
            </p>
          </div>

          <div className="so-metric-card critical">
            <h3>Critical</h3>
            <p className="so-metric-value">
              {summary?.critical ?? "—"}
            </p>
          </div>

          <div className="so-metric-card">
            <h3>Last Scan</h3>
            <p className="so-metric-value">
              {summary?.last_scan ?? "—"}
            </p>
          </div>

        </div>

        {/* EVENTS LIST */}
        <div className="so-events-card">
          <h3 className="so-events-title">Recent Events</h3>

          {events.length > 0 ? (
            <ul className="so-events-list">
              {events.map((evt, idx) => (
                <li key={idx} className="so-event-item">
                  <div className="so-event-main">
                    <strong>{evt.type}</strong> — {evt.description}
                  </div>
                  <div className="so-event-meta">
                    {evt.timestamp}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="so-panel-empty">No anomaly events detected.</p>
          )}
        </div>

      </div>
    </div>
  );
}
