import React, { useEffect, useState } from "react";

import PelmAlerts from "../components/PelmAlerts";
import PelmRegressionPanel from "../components/PelmRegressionPanel";
import PelmRiskTrend from "../components/PelmRiskTrend";
import PelmSnapshotDiff from "../components/PelmSnapshotDiff";

// ------------------------------------------------------------
// Theme Tokens (unified across dashboard)
// ------------------------------------------------------------
const COLORS = {
  bg: "#1a1a1a",
  card: "#111",
  border: "#333",
  text: "#fff",
  low: "#00e676",
  medium: "#ffb300",
  high: "#ff3b3b",
  accent: "#00eaff",
};

export default function PelmDashboard() {
  const [status, setStatus] = useState<any>(null);
  const [snapshots, setSnapshots] = useState<any[]>([]);
  const [leftSnap, setLeftSnap] = useState<string | null>(null);
  const [rightSnap, setRightSnap] = useState<string | null>(null);
  const [autoRefresh, setAutoRefresh] = useState<boolean>(false);

  // ------------------------------------------------------------
  // Loaders
  // ------------------------------------------------------------
  const loadStatus = () => {
    fetch("/pelm/status")
      .then((r) => r.json())
      .then(setStatus)
      .catch(() => setStatus(null));
  };

  const loadSnapshots = () => {
    fetch("/pelm/snapshots/list")
      .then((r) => r.json())
      .then((list) => {
        const enriched = list.map((name: string) => {
          const ts = name.replace("pelm-", "").replace(".json", "");
          return {
            name,
            timestamp: ts,
            severity: computeSeverityFromName(name),
          };
        });
        setSnapshots(enriched);
      })
      .catch(() => setSnapshots([]));
  };

  // Simple placeholder severity heuristic
  const computeSeverityFromName = (name: string) => {
    const n = name.length % 3;
    return n === 0 ? "low" : n === 1 ? "medium" : "high";
  };

  // ------------------------------------------------------------
  // Auto-refresh loop
  // ------------------------------------------------------------
  useEffect(() => {
    loadStatus();
    loadSnapshots();

    if (!autoRefresh) return;

    const id = setInterval(() => {
      loadStatus();
      loadSnapshots();
    }, 5000);

    return () => clearInterval(id);
  }, [autoRefresh]);

  if (!status) {
    return <div style={{ padding: 20 }}>Loading PELM Governance Dashboard…</div>;
  }

  // ------------------------------------------------------------
  // Compare with Latest Shortcut
  // ------------------------------------------------------------
  const compareWithLatest = () => {
    if (snapshots.length < 2) return;
    const latest = snapshots[snapshots.length - 1].name;
    const previous = snapshots[snapshots.length - 2].name;
    setLeftSnap(previous);
    setRightSnap(latest);
  };

  return (
    <div style={{ padding: 20, color: COLORS.text }}>
      <h1>PELM Governance Dashboard</h1>

      {/* -------------------------------------------------- */}
      {/* Navigation */}
      {/* -------------------------------------------------- */}
      <div style={{ marginBottom: 20 }}>
        <a href="/pelm/console" style={{ color: COLORS.accent }}>
          ← Back to PELM Console
        </a>
      </div>

      {/* -------------------------------------------------- */}
      {/* Governance Summary Card */}
      {/* -------------------------------------------------- */}
      <div
        style={{
          padding: 20,
          background: COLORS.bg,
          border: `1px solid ${COLORS.border}`,
          borderRadius: 6,
          marginBottom: 20,
        }}
      >
        <h3>Governance Summary</h3>
        <div style={{ marginTop: 10, lineHeight: "1.6em" }}>
          <strong>Current Risk:</strong> {status.risk}
          <br />
          <strong>Last Snapshot:</strong> {status.last_snapshot}
          <br />
          <strong>Total Snapshots:</strong> {snapshots.length}
        </div>

        {/* Auto-refresh toggle */}
        <div style={{ marginTop: 15 }}>
          <label style={{ cursor: "pointer" }}>
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={() => setAutoRefresh(!autoRefresh)}
              style={{ marginRight: 8 }}
            />
            Auto-refresh every 5 seconds
          </label>
        </div>
      </div>

      {/* -------------------------------------------------- */}
      {/* Alerts */}
      {/* -------------------------------------------------- */}
      <PelmAlerts />

      {/* -------------------------------------------------- */}
      {/* Regression Panel */}
      {/* -------------------------------------------------- */}
      <PelmRegressionPanel />

      {/* -------------------------------------------------- */}
      {/* Trend */}
      {/* -------------------------------------------------- */}
      <h2 style={{ marginTop: 30 }}>Risk Trend</h2>
      <PelmRiskTrend />

      {/* -------------------------------------------------- */}
      {/* Snapshot Timeline (Enhanced + Polished) */}
      {/* -------------------------------------------------- */}
      <h2 style={{ marginTop: 30 }}>Snapshot Timeline</h2>

      <div
        style={{
          display: "flex",
          gap: 12,
          flexWrap: "wrap",
          marginTop: 10,
        }}
      >
        {snapshots.map((snap) => (
          <div
            key={snap.name}
            title={`Snapshot: ${snap.name}\nTimestamp: ${snap.timestamp}\nSeverity: ${snap.severity}`}
            style={{
              padding: "8px 12px",
              background: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 6,
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
            onClick={() => {
              if (!leftSnap) setLeftSnap(snap.name);
              else if (!rightSnap) setRightSnap(snap.name);
              else {
                setLeftSnap(snap.name);
                setRightSnap(null);
              }
            }}
          >
            <span
              style={{
                width: 10,
                height: 10,
                borderRadius: "50%",
                background:
                  snap.severity === "low"
                    ? COLORS.low
                    : snap.severity === "medium"
                    ? COLORS.medium
                    : COLORS.high,
              }}
            />
            {snap.timestamp}
          </div>
        ))}
      </div>

      {/* Compare with Latest */}
      <div style={{ marginTop: 15 }}>
        <button
          onClick={compareWithLatest}
          style={{
            padding: "6px 12px",
            background: COLORS.accent,
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
            color: "#000",
            fontWeight: "bold",
          }}
        >
          Compare Latest ↔ Previous
        </button>
      </div>

      {/* -------------------------------------------------- */}
      {/* Quick Diff Selector */}
      {/* -------------------------------------------------- */}
      <h2 style={{ marginTop: 30 }}>Quick Diff</h2>
      <div style={{ marginBottom: 10 }}>
        <strong>Left:</strong> {leftSnap || "—"} <br />
        <strong>Right:</strong> {rightSnap || "—"}
      </div>

      {leftSnap && rightSnap && (
        <PelmSnapshotDiff left={leftSnap} right={rightSnap} />
      )}

      {/* -------------------------------------------------- */}
      {/* Export */}
      {/* -------------------------------------------------- */}
      <h2 style={{ marginTop: 30 }}>Export Reports</h2>
      <a href="/pelm/report/html" target="_blank" style={{ color: COLORS.accent }}>
        Download HTML Report
      </a>
      <br />
      <a
        href="/pelm/report/markdown"
        target="_blank"
        style={{ color: COLORS.accent }}
      >
        Download Markdown Report
      </a>
    </div>
  );
}
