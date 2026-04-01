import React, { useEffect, useState } from "react";

export default function HealthPredict() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/health/predict")
      .then((res) => res.json())
      .then((d) => setData(d));
  }, []);

  if (!data) return <div style={{ padding: 20 }}>Loading prediction...</div>;

  return (
    <div style={{ padding: 20 }}>
      <h1>Predictive Health Forecast</h1>

      {data.error && <p>{data.error}</p>}

      {!data.error && (
        <>
          <h2>Risk Level: {data.risk.toUpperCase()}</h2>

          <h3>Predicted Scores</h3>
          <ul>
            {Object.entries(data.predictions).map(([k, v]) => (
              <li key={k}>
                {k}: <strong>{v}</strong>
              </li>
            ))}
          </ul>

          <h3>Model Details</h3>
          <pre style={{ background: "#111", color: "#eee", padding: 12 }}>
            {JSON.stringify(data, null, 2)}
          </pre>
        </>
      )}
    </div>
  );
}
