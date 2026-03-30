import React from "react";
import { PieChart, Pie, Cell, Tooltip } from "recharts";

interface Props {
  data: { name: string; value: number }[];
}

const COLORS = ["#2ecc71", "#f1c40f", "#e74c3c"];

export default function DonutChart({ data }: Props) {
  return (
    <PieChart width={260} height={260}>
      <Pie
        data={data}
        cx="50%"
        cy="50%"
        innerRadius={60}
        outerRadius={90}
        paddingAngle={4}
        dataKey="value"
      >
        {data.map((_, i) => (
          <Cell key={i} fill={COLORS[i % COLORS.length]} />
        ))}
      </Pie>
      <Tooltip />
    </PieChart>
  );
}
