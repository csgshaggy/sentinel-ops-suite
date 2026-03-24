import React from "react";

export default function DoctorHealthWidget({ score }: { score: number }) {
  return (
    <div
      style={{
        padding: "1rem",
        background: "var(--bg-panel)",
        border: "1px solid var(--border)",
        borderRadius: "6px",
        marginBottom: "1rem",
      }}
    >
      <h3>System Health</h3>
      <div style={{ fontSize: "2rem", fontWeight: "bold" }}>{score}</div>
    </div>
  );
}
