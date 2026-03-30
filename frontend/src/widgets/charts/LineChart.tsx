import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

interface Props {
  data: { name: string; value: number }[];
}

export default function TimingLineChart({ data }: Props) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={data}>
        <XAxis dataKey="name" stroke="var(--text)" />
        <YAxis stroke="var(--text)" />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#9b59b6" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}
