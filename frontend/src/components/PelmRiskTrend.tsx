import React, { useEffect, useState } from "react";

export default function PelmRiskTrend() {
  const [trend, setTrend] = useState([]);

  useEffect(() => {
    fetch("/pelm/snapshots/trend")
      .then((r) => r.json())
      .then((data) => setTrend(data.trend || []));
  }, []);

  if (!trend.length) {
    return <div style={{ padding: 10 }}>No trend data available.</div>;
  }

  // Convert risk to numeric values for simple plotting
  const riskToValue = (risk) => {
    if (risk === "low") return 1;
    if (risk === "medium") return 2;
    if (risk === "high") return 3;
    return 0;
  };

  const points = trend.map((t, i) => ({
    x: i * 40 + 20,
    y: 120 - riskToValue(t.risk) * 30,
    label: t.risk,
    timestamp: t.timestamp,
  }));

  const path = points
    .map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`)
    .join(" ");

  return (
    <div style={{ padding: 20 }}>
      <h3>PELM Risk Trend</h3>

      <svg width={points.length * 40 + 40} height={150} style={{ border: "1px solid #444" }}>
        {/* Trend line */}
        <path d={path} stroke="#00eaff" strokeWidth="2" fill="none" />

        {/* Points */}
        {points.map((p, i) => (
          <g key={i}>
            <circle cx={p.x} cy={p.y} r="4" fill="#00eaff" />
            <text x={p.x - 10} y={p.y - 10} fill="#fff" fontSize="10">
              {p.label}
            </text>
          </g>
        ))}
      </svg>

      <div style={{ marginTop: 10 }}>
        {trend.map((t, i) => (
          <div key={i} style={{ color: "#ccc", fontSize: 12 }}>
            {t.timestamp} — {t.risk}
          </div>
        ))}
      </div>
    </div>
  );
}
