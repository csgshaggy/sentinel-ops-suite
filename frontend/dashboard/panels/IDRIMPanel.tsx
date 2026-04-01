// frontend/dashboard/panels/IDRIMPanel.tsx

import React, { useState } from "react";

export default function IDRIMPanel() {
  const [events, setEvents] = useState([]);
  const [diff, setDiff] = useState(null);
  const [baseline, setBaseline] = useState(null);
  const [loading, setLoading] = useState(false);

  const runIDRIM = async () => {
    setLoading(true);
    try {
      const res = await fetch("/idrim/run");
      const data = await res.json();
      setEvents(data.events || []);
    } catch (err) {
      console.error("IDRIM run failed:", err);
    }
    setLoading(false);
  };

  const rebuildBaseline = async () => {
    setLoading(true);
    try {
      const res = await fetch("/idrim/baseline/rebuild", { method: "POST" });
      const data = await res.json();
      setBaseline(data.baseline || null);
    } catch (err) {
      console.error("Baseline rebuild failed:", err);
    }
    setLoading(false);
  };

  const loadDiff = async () => {
    setLoading(true);
    try {
      const res = await fetch("/idrim/diff");
      const data = await res.json();
      setDiff(data.diff || null);
    } catch (err) {
      console.error("Diff load failed:", err);
    }
    setLoading(false);
  };

  const severityColor = (severity: string) => {
    switch (severity) {
      case "high":
        return "bg-red-600 text-white px-2 py-1 rounded";
      case "medium":
        return "bg-yellow-500 text-black px-2 py-1 rounded";
      default:
        return "bg-gray-600 text-white px-2 py-1 rounded";
    }
  };

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold">IDRIM — IAM Drift & Role Integrity Monitor</h1>

      {/* Controls */}
      <div className="flex space-x-4">
        <button
          onClick={runIDRIM}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Run IDRIM
        </button>

        <button
          onClick={rebuildBaseline}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Rebuild Baseline
        </button>

        <button
          onClick={loadDiff}
          className="bg-purple-600 text-white px-4 py-2 rounded"
        >
          View Diff
        </button>
      </div>

      {loading && <div className="text-gray-400">Processing…</div>}

      {/* Drift Events */}
      <div>
        <h2 className="text-xl font-semibold mt-6">Drift Events</h2>
        {events.length === 0 ? (
          <div className="text-gray-400">No events detected.</div>
        ) : (
          <table className="w-full mt-2 border-collapse">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="text-left p-2">User</th>
                <th className="text-left p-2">Type</th>
                <th className="text-left p-2">Severity</th>
                <th className="text-left p-2">Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {events.map((ev, idx) => (
                <tr key={idx} className="border-b border-gray-800">
                  <td className="p-2">{ev.user}</td>
                  <td className="p-2">{ev.type}</td>
                  <td className="p-2">
                    <span className={severityColor(ev.severity)}>
                      {ev.severity}
                    </span>
                  </td>
                  <td className="p-2">{ev.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Diff Viewer */}
      {diff && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">IAM Diff</h2>
          <pre className="bg-black text-green-400 p-4 rounded mt-2 overflow-auto max-h-96">
            {JSON.stringify(diff, null, 2)}
          </pre>
        </div>
      )}

      {/* Baseline Viewer */}
      {baseline && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">New Baseline</h2>
          <pre className="bg-black text-blue-400 p-4 rounded mt-2 overflow-auto max-h-96">
            {JSON.stringify(baseline, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
