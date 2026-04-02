import React, { useEffect,useState } from "react";

export default function PelmSnapshotDiff() {
  const [left, setLeft] = useState("");
  const [right, setRight] = useState("");
  const [snapshots, setSnapshots] = useState<string[]>([]);
  const [diff, setDiff] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/pelm/snapshots/list")
      .then((r) => r.json())
      .then((data) => setSnapshots(data || []))
      .catch(() => setSnapshots([]));
  }, []);

  const runDiff = () => {
    if (!left || !right) {
      setError("Select both snapshots before diffing.");
      return;
    }

    setError("");

    fetch(`/pelm/snapshots/diff?left=${left}&right=${right}`)
      .then((r) => r.json())
      .then((data) => setDiff(data))
      .catch(() => setError("Failed to load diff."));
  };

  return (
    <div style={{ padding: 20 }}>
      <h3>Snapshot Diff Viewer</h3>

      {/* Snapshot selectors */}
      <div style={{ marginBottom: 10 }}>
        <label style={{ marginRight: 10 }}>Left Snapshot:</label>
        <select
          value={left}
          onChange={(e) => setLeft(e.target.value)}
          style={{ width: 260 }}
        >
          <option value="">Select snapshot…</option>
          {snapshots.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </div>

      <div style={{ marginBottom: 10 }}>
        <label style={{ marginRight: 10 }}>Right Snapshot:</label>
        <select
          value={right}
          onChange={(e) => setRight(e.target.value)}
          style={{ width: 260 }}
        >
          <option value="">Select snapshot…</option>
          {snapshots.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </div>

      <button onClick={runDiff}>Run Diff</button>

      {error && (
        <div style={{ color: "red", marginTop: 10 }}>
          {error}
        </div>
      )}

      {!diff && !error && (
        <div style={{ marginTop: 20, color: "#aaa" }}>
          Select two snapshots to compare.
        </div>
      )}

      {diff && (
        <div style={{ marginTop: 20 }}>
          <h4>Risk</h4>
          <pre style={{ background: "#222", padding: 10 }}>
            {JSON.stringify(diff.risk, null, 2)}
          </pre>

          <h4>Status</h4>
          <pre style={{ background: "#222", padding: 10 }}>
            {JSON.stringify(diff.status, null, 2)}
          </pre>

          <h4>Signals</h4>
          <pre style={{ background: "#222", padding: 10 }}>
            {JSON.stringify(diff.signals, null, 2)}
          </pre>

          <h4>Metadata</h4>
          <pre style={{ background: "#222", padding: 10 }}>
            {JSON.stringify(diff.metadata, null, 2)}
          </pre>

          <h4>Raw Snapshots</h4>
          <pre style={{ background: "#111", padding: 10 }}>
            {JSON.stringify(diff.raw, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
