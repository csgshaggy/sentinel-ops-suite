// dashboard/src/components/DetailDrawer.tsx

import React, { useEffect, useState } from "react";
import { Plugin } from "../types";
import { fetchPluginLogs } from "../api/client";
import LogsViewer from "./LogsViewer";
import useAutoRefresh from "../hooks/useAutoRefresh";

export default function DetailDrawer({
  plugin,
  onClose,
}: {
  plugin: Plugin | null;
  onClose: () => void;
}) {
  const [logs, setLogs] = useState<string[]>([]);
  const [running, setRunning] = useState(false);
  const [runResult, setRunResult] = useState<any>(null);

  // Initial load
  useEffect(() => {
    if (!plugin) return;

    const loadLogs = async () => {
      try {
        const data = await fetchPluginLogs(plugin.id);
        setLogs(data);
      } catch {
        setLogs(["Failed to load logs."]);
      }
    };

    loadLogs();
  }, [plugin]);

  // Real-time polling (1 second)
  useAutoRefresh(() => {
    if (plugin) {
      fetchPluginLogs(plugin.id)
        .then(setLogs)
        .catch(() => setLogs(["Failed to load logs."]));
    }
  }, 1000);

  if (!plugin) return null;

  const runPlugin = async () => {
    setRunning(true);
    setRunResult(null);

    try {
      const res = await fetch(
        `http://127.0.0.1:5001/api/plugins/${plugin.id}/run`,
        {
          method: "POST",
        }
      );
      const data = await res.json();
      setRunResult(data);
    } catch (err) {
      setRunResult({ error: "Failed to run plugin" });
    }

    setRunning(false);
  };

  return (
    <div
      style={{
        position: "fixed",
        right: 0,
        top: 0,
        bottom: 0,
        width: "360px",
        background: "var(--bg-panel)",
        borderLeft: "1px solid var(--border)",
        padding: "1rem",
        overflowY: "auto",
        boxShadow: "-4px 0 12px rgba(0,0,0,0.4)",
        zIndex: 1000,
      }}
    >
      <button
        onClick={onClose}
        style={{
          float: "right",
          background: "transparent",
          border: "none",
          color: "var(--text)",
          fontSize: "1.2rem",
          cursor: "pointer",
        }}
      >
        ✕
      </button>

      <h2>{plugin.name}</h2>

      <p>
        <strong>Category:</strong> {plugin.category}
      </p>
      <p>
        <strong>Status:</strong> {plugin.status}
      </p>
      <p>
        <strong>Avg Duration:</strong> {plugin.avgDurationMs} ms
      </p>
      <p>
        <strong>Last Run:</strong> {new Date(plugin.lastRunAt).toLocaleString()}
      </p>

      <button
        onClick={runPlugin}
        disabled={running}
        style={{
          marginTop: "1rem",
          padding: "0.5rem 1rem",
          background: running ? "#777" : "#4a90e2",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: running ? "not-allowed" : "pointer",
        }}
      >
        {running ? "Running…" : "Run Plugin"}
      </button>

      {runResult && (
        <pre
          style={{
            marginTop: "1rem",
            background: "#1e1e1e",
            color: "#dcdcdc",
            padding: "0.75rem",
            borderRadius: "6px",
            maxHeight: "200px",
            overflowY: "auto",
          }}
        >
          {JSON.stringify(runResult, null, 2)}
        </pre>
      )}

      <h3 style={{ marginTop: "2rem" }}>Logs</h3>
      <LogsViewer logs={logs} />
    </div>
  );
}
