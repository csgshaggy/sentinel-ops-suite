// dashboard/src/components/CategoryFilterBar.tsx

import React from "react";

interface Props {
  value: string;
  onChange: (v: string) => void;
  categories: string[];
}

export default function CategoryFilterBar({
  value,
  onChange,
  categories,
}: Props) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{ padding: "0.5rem" }}
    >
      <option value="all">All Categories</option>

      {categories.map((cat) => (
        <option key={cat} value={cat}>
          {cat}
        </option>
      ))}
    </select>
  );
}
