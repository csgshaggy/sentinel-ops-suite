import React from "react";
import { TimingBucket } from "../types";

interface Props {
  buckets: TimingBucket[];
}

export default function TimingHeatmap({ buckets }: Props) {
  if (!buckets.length) return <div>No timing data.</div>;

  const max = Math.max(...buckets.map((b) => b.count));

  return (
    <div>
      <h2>Execution Timing Heatmap</h2>
      <div style={{ display: "flex", gap: "0.5rem" }}>
        {buckets.map((b) => {
          const intensity = b.count / max;
          return (
            <div
              key={b.label}
              style={{
                padding: "0.5rem",
                background: `rgba(0, 200, 255, ${0.2 + intensity * 0.6})`,
              }}
            >
              <div>{b.label}</div>
              <div>{b.count} runs</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
