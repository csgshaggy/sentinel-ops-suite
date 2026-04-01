import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

export default function HealthTrend() {
  const [trend, setTrend] = useState<any[]>([]);

  useEffect(() => {
    fetch("/health/trend")
      .then((res) => res.json())
      .then((data) => setTrend(data));
  }, []);

  if (!trend.length) {
    return (
      <div style={{ padding: "20px" }}>
        <h1>Health Trend</h1>
        <p>No trend data available yet.</p>
      </div>
    );
  }

  const labels = trend.map((t) =>
    new Date(t.timestamp * 1000).toLocaleString()
  );

  const data = {
    labels,
    datasets: [
      {
        label: "Health Score",
        data: trend.map((t) => t.score),
        borderColor: "#4ade80",
        backgroundColor: "rgba(74, 222, 128, 0.3)",
        tension: 0.3,
      },
      {
        label: "CPU %",
        data: trend.map((t) => t.cpu),
        borderColor: "#60a5fa",
        backgroundColor: "rgba(96, 165, 250, 0.3)",
        tension: 0.3,
      },
      {
        label: "Memory %",
        data: trend.map((t) => t.memory),
        borderColor: "#f87171",
        backgroundColor: "rgba(248, 113, 113, 0.3)",
        tension: 0.3,
      },
      {
        label: "Disk %",
        data: trend.map((t) => t.disk),
        borderColor: "#fbbf24",
        backgroundColor: "rgba(251, 191, 36, 0.3)",
        tension: 0.3,
      },
    ],
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Health Trend</h1>
      <Line data={data} />
    </div>
  );
}
