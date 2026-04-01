import React, { useState } from "react";

export default function AnomalyCorrelation() {
  const [timestamp, setTimestamp] = useState("");
  const [result, setResult] = useState(null);

  const runCorrelation = () => {
    fetch(`/anomaly/correlate?ts=${timestamp}`)
      .then((res) => res.json())
      .then((data) => setResult(data));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Anomaly Correlation</h1>

      <input
        type="text"
        placeholder="Enter anomaly timestamp"
        value={timestamp}
        onChange={(e) => setTimestamp(e.target.value)}
        style={{ marginRight: "10px" }}
      />

      <button onClick={runCorrelation}>Correlate</button>

      <pre style={{ marginTop: "20px" }}>
        {result ? JSON.stringify(result, null, 2) : "No results yet."}
      </pre>
    </div>
  );
}
