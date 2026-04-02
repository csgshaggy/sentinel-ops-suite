import React, { useEffect, useState } from "react";

import SeverityBadge from "./SeverityBadge";

export default function PelmRegressionPanel() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("/pelm/regression")
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData(null));
  }, []);

  if (!data) {
    return <div style={{ padding: 10 }}>Loading regression analytics…</div>;
  }

  const { regression_score, drift_detected, risk_delta, risk_acceleration, risk_trend } = data;

  // Sparkline points
  const points = risk_trend.map((v: number, i: number) => ({
    x: i * 25 + 10,
    y: 60 - v * 12,
  }));

  const path = points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ");

  return (
    <div
      style={{
        padding: 20,
        border: "1px solid #444",
        borderRadius: 6,
        marginTop: 20,
        background: "#1a1a1a",
      }}
    >
      <h3>PELM Regression Analysis</h3>

      {/* -------------------------------------------------- */}
      {/* Regression Score */}
      {/* -------------------------------------------------- */}
      <div style={{ marginBottom: 10 }}>
        <span style={{ fontSize: 18, marginRight: 10 }}>Regression Score:</span>
        <SeverityBadge value={regression_score} />
      </div>

      {/* -------------------------------------------------- */}
      {/* Drift */}
      {/* -------------------------------------------------- */}
      <div style={{ marginBottom: 10 }}>
        <strong>Drift Detected:</strong>{" "}
        <span style={{ color: drift_detected ? "#ff3b3b" : "#00e676" }}>
          {drift_detected ? "YES" : "NO"}
        </span>
      </div>

      {/* -------------------------------------------------- */}
      {/* Delta + Acceleration */}
      {/* -------------------------------------------------- */}
      <div style={{ marginBottom: 10 }}>
        <strong>Risk Delta:</strong> {risk_delta}
        <br />
        <strong>Risk Acceleration:</strong> {risk_acceleration}
      </div>

      {/* -------------------------------------------------- */}
      {/* Sparkline */}
      {/* -------------------------------------------------- */}
      <div style={{ marginTop: 20 }}>
        <strong>Risk Trend:</strong>
        <br />
        <svg width={points.length * 25 + 20} height={80}>
          <path d={path} stroke="#00eaff" strokeWidth="2" fill="none" />
          {points.map((p, i) => (
            <circle key={i} cx={p.x} cy={p.y} r="3" fill="#00eaff" />
          ))}
        </svg>
      </div>

      {/* -------------------------------------------------- */}
      {/* Raw Metrics */}
      {/* -------------------------------------------------- */}
      <div style={{ marginTop: 20 }}>
        <strong>Raw Metrics</strong>
        <pre style={{ background: "#111", padding: 10 }}>{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  );
}
