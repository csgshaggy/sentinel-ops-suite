// =====================================================================
// SSRF Command Console — Admin Audit Logs Page
// Session Cookie Auth • Forensic Event Viewer
// =====================================================================

import { useEffect, useState } from "react";
import { fetchAuditLogs } from "../../api/admin";
import Table from "../../components/Table";

export default function AdminAuditLogs() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchAuditLogs();
        const rows = data.map((l) => ({
          timestamp: new Date(l.timestamp).toLocaleString(),
          actor_email: l.actor_email || "-",
          action: l.action,
          target: l.target || "-",
          details: l.details || "-",
        }));
        setLogs(rows);
      } catch {
        setError("Failed to load audit logs");
      }
    }
    load();
  }, []);

  return (
    <div className="panel" style={{ margin: "2rem" }}>
      <h2>Audit Logs</h2>

      {error && <div className="error">{error}</div>}

      <Table
        columns={["timestamp", "actor_email", "action", "target", "details"]}
        data={logs}
      />
    </div>
  );
}
