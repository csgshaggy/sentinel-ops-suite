import React, { useEffect, useState } from "react";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch("/alerts")
      .then((res) => res.json())
      .then((data) => setAlerts(data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Operator Alerts</h1>

      {alerts.length === 0 && <p>No active alerts.</p>}

      {alerts.map((a, i) => (
        <div
          key={i}
          style={{
            padding: "10px",
            marginBottom: "10px",
            borderRadius: "6px",
            background:
              a.severity === "high" ? "#7f1d1d" : a.severity === "medium" ? "#78350f" : "#1e3a8a",
            color: "white",
          }}
        >
          <strong>{a.type}</strong>
          <div>{a.message}</div>
        </div>
      ))}
    </div>
  );
}
