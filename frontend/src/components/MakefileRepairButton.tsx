import React, { useState } from "react";

export const MakefileRepairButton: React.FC = () => {
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const heal = async () => {
    setLoading(true);
    setStatus(null);
    try {
      const res = await fetch("/api/makefile/heal", { method: "POST" });
      const json = await res.json();
      setStatus(json.message || "Repaired");
    } catch (e: any) {
      setStatus("Error repairing Makefile");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "1rem" }}>
      <button
        onClick={heal}
        disabled={loading}
        style={{
          padding: "0.5rem 1rem",
          background: "#3498db",
          color: "white",
          border: "none",
          borderRadius: 6,
          cursor: "pointer",
        }}
      >
        {loading ? "Repairing…" : "Repair Makefile"}
      </button>
      {status && <div style={{ marginTop: 8 }}>{status}</div>}
    </div>
  );
};
