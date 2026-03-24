// dashboard/src/components/TimingHeatmap.tsx

import React from "react";
import { TimingBucket } from "../types";

interface Props {
  buckets: TimingBucket[];
}

export default function TimingHeatmap({ buckets }: Props) {
  if (!buckets.length) {
    return <div style={{ color: "#888" }}>No timing data available.</div>;
  }

  const max = Math.max(...buckets.map((b) => b.count)) || 1;

  return (
    <div>
      <h2>Execution Timing Heatmap</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(80px, 1fr))",
          gap: "0.5rem",
        }}
      >
        {buckets.map((b) => {
          const intensity = b.count / max;
          const bg = `rgba(0, 200, 255, ${0.15 + intensity * 0.7})`;

          return (
            <div
              key={b.label}
              style={{
                padding: "0.5rem",
                borderRadius: "0.5rem",
                background: bg,
                border: "1px solid #144",
                textAlign: "center",
                fontSize: "0.8rem",
              }}
            >
              <div style={{ fontWeight: 600 }}>{b.label}</div>
              <div>{b.count} runs</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
