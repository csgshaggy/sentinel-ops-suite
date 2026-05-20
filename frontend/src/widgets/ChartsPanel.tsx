import React from "react";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { TimingBucket } from "../types";

export default function ChartsPanel({ timing }: { timing: TimingBucket[] }) {
  return (
    <div style={{ height: "240px", marginBottom: "1rem" }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={timing}>
          <XAxis dataKey="bucket" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#4a90e2" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
