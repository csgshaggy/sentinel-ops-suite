import React from "react";

export default function SeverityBadge({ value }: { value: number }) {
  let color = "#00e676"; // green (good)

  if (value >= 70) {
    color = "#ff3b3b"; // red (bad)
  } else if (value >= 40) {
    color = "#ffb300"; // yellow (warning)
  }

  return (
    <span
      style={{
        padding: "4px 10px",
        background: color,
        borderRadius: 4,
        color: "#000",
        fontWeight: "bold",
        marginLeft: 8,
      }}
    >
      {value}
    </span>
  );
}
