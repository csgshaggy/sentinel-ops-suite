import React, { useEffect, useState } from "react";
import PelmRiskTrend from "../components/PelmRiskTrend";
import PelmSnapshotDiff from "../components/PelmSnapshotDiff";
import PelmRegressionPanel from "../components/PelmRegressionPanel";
import PelmAlerts from "../components/PelmAlerts";

export default function PelmConsole() {
  const [status, setStatus] = useState(null);
  const [snapshots, setSnapshots] = useState([]);
  const [selectedSnapshot, setSelectedSnapshot] = useState(null);

  const loadStatus = () => {
    fetch("/pelm/status")
      .then((r) => r.json())
      .then(setStatus);
  };

  const loadSnapshots = () => {
    fetch("/pelm/snapshots/list")
      .then((r) => r.json())
      .then(setSnapshots);
  };

  const loadSnapshot = (name) => {
    fetch(`/pelm/snapshots/get/${name}`)
      .then((r) => r.json())
      .then(setSelectedSnapshot);
  };

  const runPelm = () => {
    fetch("/pelm/run")
      .then((r) => r.json())
      .then(() => {
        loadStatus();
        loadSnapshots();
      });
  };

  const repairPelm = () => {
    fetch("/pelm/governance/repair", { method: "POST" })
      .then((r) => r.json())
      .then(loadStatus);
  };

  useEffect(() => {
    loadStatus();
    loadSnapshots();
  }, []);

  if (!status) return <div style={{ padding: 20 }}>Loading PELM Console…</div>;

  return (
    <div style={{ padding: 20 }}>
      <h1>PELM Console</h1>

      {/* -------------------------------------------------- */}
      {/* Controls */}
      {/* -------------------------------------------------- */}
      <div style={{ marginBottom: 20 }}>
        <button onClick={runPelm}>Run PELM</button>
        <button onClick={repairPelm} style={{ marginLeft: 10 }}>
          Repair PELM
        </button>
      </div>

      {/* -------------------------------------------------- */}
      {/* Status */}
      {/* -------------------------------------------------- */}
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>

      {/* -------------------------------------------------- */}
      {/* Alerts (NEW) */}
      {/* -------------------------------------------------- */}
      <PelmAlerts />

      {/* -------------------------------------------------- */}
      {/* Regression Panel */}
      {/* -------------------------------------------------- */}
      <PelmRegressionPanel />

      {/* -------------------------------------------------- */}
      {/* Risk Trend */}
      {/* -------------------------------------------------- */}
      <h2>Risk Trend</h2>
      <PelmRiskTrend />

      {/* -------------------------------------------------- */}
      {/* Snapshot List */}
      {/* -------------------------------------------------- */}
      <h2>Snapshots</h2>
      <ul>
        {snapshots.map((s) => (
          <li key={s}>
            <button
              onClick={() => {
                loadSnapshot(s);
                setSelectedSnapshot({ filename: s });
              }}
            >
              {s}
            </button>
          </li>
        ))}
      </ul>

      {/* -------------------------------------------------- */}
      {/* Snapshot Viewer */}
      {/* -------------------------------------------------- */}
      {selectedSnapshot && (
        <>
          <h2>Snapshot: {selectedSnapshot.filename}</h2>
          <pre>{JSON.stringify(selectedSnapshot, null, 2)}</pre>
        </>
      )}

      {/* -------------------------------------------------- */}
      {/* Snapshot Diff Viewer */}
      {/* -------------------------------------------------- */}
      <h2>Snapshot Diff</h2>
      <PelmSnapshotDiff />

      {/* -------------------------------------------------- */}
      {/* Export */}
      {/* -------------------------------------------------- */}
      <h2>Export</h2>
      <a href="/pelm/report/html" target="_blank">Download HTML Report</a>
      <br />
      <a href="/pelm/report/markdown" target="_blank">Download Markdown Report</a>
    </div>
  );
}
