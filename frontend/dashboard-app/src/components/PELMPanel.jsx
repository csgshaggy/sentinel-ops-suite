import React, { useEffect, useState } from "react";
import "./../styles/panel-shell.css";

export default function PELMPanel() {
  const [summary, setSummary] = useState(null);
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        const res1 = await fetch("/api/pelm/summary", {
          method: "GET",
          credentials: "include",
        });

        const res2 = await fetch("/api/pelm/details", {
          method: "GET",
          credentials: "include",
        });

        if (!res1.ok || !res2.ok) throw new Error("bad response");

        const data1 = await res1.json();
        const data2 = await res2.json();

        if (isMounted) {
          setSummary(data1);
          setDetails(data2);
        }
      } catch (err) {
        if (isMounted) {
          setSummary(null);
          setDetails(null);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="panel-shell">
        <h2 className="panel-title">PELM Panel</h2>
        <p className="panel-loading">Loading…</p>
      </div>
    );
  }

  return (
    <div className="panel-shell">
      <h2 className="panel-title">PELM Panel</h2>

      {/* SUMMARY GRID */}
      <div className="panel-grid">
        <div className="panel-card">
          <h3 className="panel-section-title">Total Events</h3>
          <p className="panel-metric">
            {summary?.total_events ?? "—"}
          </p>
        </div>

        <div className="panel-card">
          <h3 className="panel-section-title">Critical Alerts</h3>
          <p className="panel-metric critical">
            {summary?.critical_alerts ?? "—"}
          </p>
        </div>

        <div className="panel-card">
          <h3 className="panel-section-title">Last Updated</h3>
          <p className="panel-metric">
            {summary?.last_updated ?? "—"}
          </p>
        </div>
      </div>

      {/* DETAILS */}
      <div className="panel-card" style={{ marginTop: "20px" }}>
        <h3 className="panel-section-title">Details</h3>

        {details?.items?.length > 0 ? (
          <ul className="panel-list">
            {details.items.map((item, idx) => (
              <li key={idx} className="panel-list-item">
                <strong>{item.name}</strong>: {item.value}
              </li>
            ))}
          </ul>
        ) : (
          <p className="panel-empty">No details available.</p>
        )}
      </div>
    </div>
  );
}
