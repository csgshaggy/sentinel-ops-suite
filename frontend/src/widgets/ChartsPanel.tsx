import React from "react";
import { TimingBucket } from "../types";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

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
