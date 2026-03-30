import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

interface Props {
  data: { name: string; value: number }[];
}

export default function CategoryBarChart({ data }: Props) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data}>
        <XAxis dataKey="name" stroke="var(--text)" />
        <YAxis stroke="var(--text)" />
        <Tooltip />
        <Bar dataKey="value" fill="#3498db" />
      </BarChart>
    </ResponsiveContainer>
  );
}
