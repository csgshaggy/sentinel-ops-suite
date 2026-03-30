import React from "react";
import { Plugin } from "../types";

interface Props {
  plugins: Plugin[];
  onSelect: (plugin: Plugin) => void;
}

export default function PluginTable({ plugins, onSelect }: Props) {
  return (
    <table style={{ width: "100%", marginTop: "1rem" }}>
      <thead>
        <tr>
          <th align="left">Name</th>
          <th align="left">Category</th>
          <th align="left">Status</th>
          <th align="left">Avg Duration</th>
        </tr>
      </thead>
      <tbody>
        {plugins.map((p) => (
          <tr key={p.id} onClick={() => onSelect(p)} style={{ cursor: "pointer" }}>
            <td>{p.name}</td>
            <td>{p.category}</td>
            <td>{p.status}</td>
            <td>{p.avgDurationMs} ms</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
