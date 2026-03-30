// dashboard/src/components/StatusPill.tsx

import React from "react";

export default function StatusPill({ status }: { status: string }) {
  const colors: Record<string, string> = {
    healthy: "#2ecc71",
    warning: "#f1c40f",
    error: "#e74c3c",
  };

  return (
    <span
      style={{
        padding: "0.2rem 0.6rem",
        borderRadius: "999px",
        background: colors[status] || "#555",
        color: "#000",
        fontWeight: 600,
        fontSize: "0.75rem",
      }}
    >
      {status}
    </span>
  );
}
