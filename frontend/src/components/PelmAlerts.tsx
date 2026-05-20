import React, { useEffect, useState } from "react";

import SeverityBadge from "./SeverityBadge";

export default function PelmAlerts() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("/pelm/regression")
      .then((r) => r.json())
      .then(setData)
      .catch(() => setData(null));
  }, []);

  if (!data) {
    return null; // Silent until data loads
  }

  const { regression_score, drift_detected, risk_delta, risk_acceleration } = data;

  // Determine alert severity
  const alerts: { level: "info" | "warn" | "crit"; msg: string }[] = [];

  if (drift_detected) {
    alerts.push({
      level: "crit",
      msg: "Snapshot drift detected — signals changed between snapshots.",
    });
  }

  if (regression_score >= 70) {
    alerts.push({
      level: "crit",
      msg: "Severe regression detected — system behavior is degrading rapidly.",
    });
  } else if (regression_score >= 40) {
    alerts.push({
      level: "warn",
      msg: "Moderate regression detected — monitor system behavior closely.",
    });
  }

  if (risk_acceleration > 1) {
    alerts.push({
      level: "warn",
      msg: "Risk acceleration increasing — recent snapshots show worsening trend.",
    });
  }

  if (risk_delta > 1) {
    alerts.push({
      level: "info",
      msg: "Risk level has increased over time.",
    });
  }

  if (alerts.length === 0) {
    return (
      <div
        style={{
          padding: 12,
          marginTop: 20,
          border: "1px solid #333",
          borderRadius: 6,
          background: "#0f1a0f",
          color: "#00e676",
        }}
      >
        <strong>PELM Status:</strong> No alerts. System behavior is stable.
      </div>
    );
  }

  return (
    <div
      style={{
        padding: 12,
        marginTop: 20,
        border: "1px solid #333",
        borderRadius: 6,
        background: "#1a1a1a",
      }}
    >
      <strong style={{ fontSize: 16 }}>PELM Alerts</strong>

      {alerts.map((a, i) => {
        const color = a.level === "crit" ? "#ff3b3b" : a.level === "warn" ? "#ffb300" : "#00eaff";

        return (
          <div
            key={i}
            style={{
              marginTop: 10,
              padding: "8px 10px",
              borderLeft: `4px solid ${color}`,
              background: "#111",
              borderRadius: 4,
            }}
          >
            <span style={{ color }}>{a.msg}</span>
          </div>
        );
      })}

      {/* Regression score badge */}
      <div style={{ marginTop: 12 }}>
        <strong>Regression Score:</strong>
        <SeverityBadge value={regression_score} />
      </div>
    </div>
  );
}
