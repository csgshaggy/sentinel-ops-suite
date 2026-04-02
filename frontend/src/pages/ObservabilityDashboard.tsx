import React, { useEffect, useState } from "react";

type ObservabilityData = {
  health: any;
  trend: any[];
  prediction: any;
  alerts: any[];
  makefile: any;
  latest_anomaly_correlation: any;
  pelm: any;
};

export default function ObservabilityDashboard() {
  const [data, setData] = useState<ObservabilityData | null>(null);

  useEffect(() => {
    fetch("/observability/summary")
      .then((res) => res.json())
      .then((d) => setData(d));
  }, []);

  if (!data) return <div style={{ padding: 20 }}>Loading observability data...</div>;

  const { health, trend, prediction, alerts, makefile, latest_anomaly_correlation, pelm } = data;

  return (
    <div style={{ padding: 20 }}>
      <h1>Observability Dashboard</h1>

      {/* Health Score */}
      <section>
        <h2>Current Health Score</h2>
        <div style={{ fontSize: 32, fontWeight: "bold" }}>{health.score}</div>
      </section>

      {/* Prediction */}
      <section>
        <h2>Predictive Risk</h2>
        <div>
          Risk Level: <strong>{prediction.risk.toUpperCase()}</strong>
        </div>
        <pre>{JSON.stringify(prediction.predictions, null, 2)}</pre>
      </section>

      {/* Alerts */}
      <section>
        <h2>Active Alerts</h2>
        {alerts.length === 0 && <p>No active alerts.</p>}
        {alerts.map((a, i) => (
          <div key={i} style={{ marginBottom: 8 }}>
            <strong>{a.type}</strong>: {a.message}
          </div>
        ))}
      </section>

      {/* Makefile Status */}
      <section>
        <h2>Makefile Status</h2>
        <pre>{JSON.stringify(makefile, null, 2)}</pre>
      </section>

      {/* PELM Governance */}
      <section>
        <h2>PELM Governance</h2>
        <pre>{JSON.stringify(pelm, null, 2)}</pre>
      </section>

      {/* Anomaly Correlation */}
      <section>
        <h2>Latest Anomaly Correlation</h2>
        <pre>{JSON.stringify(latest_anomaly_correlation, null, 2)}</pre>
      </section>

      {/* Trend */}
      <section>
        <h2>Recent Trend (Last 20 Points)</h2>
        <pre>{JSON.stringify(trend, null, 2)}</pre>
      </section>
    </div>
  );
}
