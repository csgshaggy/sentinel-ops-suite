import React, { useEffect, useState } from "react";

type OpsState = {
  anomaly: number;
  idrim: string;
  pelm: number;
  heartbeat: number;
};

export default function OpsConsole() {
  const [state, setState] = useState<OpsState>({
    anomaly: 0,
    idrim: "none",
    pelm: 1,
    heartbeat: 0,
  });

  useEffect(() => {
    const stream = new EventSource("/stream/ops");

    stream.onmessage = (e) => {
      const [key, value] = e.data.split("=");
      setState((prev) => ({
        ...prev,
        [key]: isNaN(Number(value)) ? value : Number(value),
      }));
    };

    return () => stream.close();
  }, []);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Unified Ops Console</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <Card title="Anomaly Score" value={state.anomaly} color="bg-red-600" />
        <Card title="IDRIM Drift" value={state.idrim} color="bg-blue-600" />
        <Card title="PELM Risk" value={state.pelm} color="bg-yellow-600" />

      </div>
    </div>
  );
}

function Card({
  title,
  value,
  color,
}: {
  title: string;
  value: any;
  color: string;
}) {
  return (
    <div className={`p-4 rounded shadow text-white ${color}`}>
      <h2 className="text-xl font-semibold">{title}</h2>
      <div className="text-3xl font-bold mt-2">{value}</div>
    </div>
  );
}
