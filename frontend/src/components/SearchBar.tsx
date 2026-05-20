import React from "react";

export default function SearchBar({
  value,
  onChange,
}: {
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <input
      type="text"
      placeholder="Search plugins..."
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{
        padding: "0.5rem",
        width: "240px",
        marginRight: "1rem",
      }}
    />
  );
}
