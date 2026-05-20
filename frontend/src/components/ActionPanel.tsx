import React, { useState } from "react";

interface ActionItem {
  id: string;
  label: string;
  endpoint: string;
  method: "GET" | "POST";
}

const actions: ActionItem[] = [
  {
    id: "refresh-dashboard",
    label: "Refresh Dashboard",
    endpoint: "/health",
    method: "GET",
  },
  {
    id: "fetch-logs",
    label: "Fetch Logs",
    endpoint: "/logs",
    method: "GET",
  },
  {
    id: "run-anomaly-scan",
    label: "Run Anomaly Scan",
    endpoint: "/anomalies/scan",
    method: "POST",
  },

  // ---------------------------------------------------------
  // PELM MODULE ACTIONS (Step 10 requirement)
  // ---------------------------------------------------------
  {
    id: "pelm-health",
    label: "Run PELM Health Check",
    endpoint: "/pelm/health",
    method: "GET",
  },
  {
    id: "pelm-stream",
    label: "Start PELM Stream",
    endpoint: "/pelm/stream",
    method: "GET",
  },
  {
    id: "pelm-plugin",
    label: "Run PELM Plugin",
    endpoint: "/pelm/plugin",
    method: "POST",
  },
];

export default function ActionPanel() {
  const [output, setOutput] = useState<string>("");

  const runAction = async (action: ActionItem) => {
    setOutput(`Running: ${action.label}...`);

    try {
      const response = await fetch(action.endpoint, {
        method: action.method,
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json().catch(() => ({
        error: "Invalid JSON response",
      }));

      setOutput(JSON.stringify(data, null, 2));
    } catch (err) {
      setOutput(`Error: ${(err as Error).message}`);
    }
  };

  return (
    <div className="action-panel" style={{ padding: "20px" }}>
      <h2>Actions</h2>

      <div className="action-buttons" style={{ marginBottom: "20px" }}>
        {actions.map((action) => (
          <button
            key={action.id}
            onClick={() => runAction(action)}
            style={{
              marginRight: "10px",
              marginBottom: "10px",
              padding: "10px 14px",
              cursor: "pointer",
            }}
          >
            {action.label}
          </button>
        ))}
      </div>

      <h3>Output</h3>
      <pre
        style={{
          background: "#111",
          color: "#0f0",
          padding: "15px",
          borderRadius: "6px",
          minHeight: "200px",
          overflowX: "auto",
        }}
      >
        {output}
      </pre>
    </div>
  );
}
