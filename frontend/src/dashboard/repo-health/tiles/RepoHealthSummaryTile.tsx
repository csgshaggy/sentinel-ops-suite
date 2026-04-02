import React from "react";

interface Props {
  score: number;
  status: string;
  breakdown: Record<string, number>;
}

export function RepoHealthSummaryTile({ score, status, breakdown }: Props) {
  const color =
    status === "excellent"
      ? "#2ecc71"
      : status === "good"
      ? "#3498db"
      : status === "warning"
      ? "#f1c40f"
      : "#e74c3c";

  return (
    <div className="tile" style={{ borderLeft: `6px solid ${color}` }}>
      <h2>Repo Health Summary</h2>

      <div style={{ fontSize: "2rem", fontWeight: "bold", color }}>
        {score}%
      </div>

      <div style={{ marginBottom: "1rem" }}>
        Status: <strong>{status}</strong>
      </div>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {Object.entries(breakdown).map(([key, val]) => (
          <li key={key}>
            {key}: <strong>{val}%</strong>
          </li>
        ))}
      </ul>
    </div>
  );
}
