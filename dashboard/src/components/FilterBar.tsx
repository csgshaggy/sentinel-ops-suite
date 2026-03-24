import React from "react";

export default function FilterBar({
  value,
  onChange,
}: {
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{ marginRight: "1rem", padding: "0.5rem" }}
    >
      <option value="all">All Statuses</option>
      <option value="ok">OK</option>
      <option value="error">Error</option>
    </select>
  );
}
