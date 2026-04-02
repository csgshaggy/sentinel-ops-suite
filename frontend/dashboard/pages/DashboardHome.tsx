import React, { useEffect, useState } from "react";

export default function DashboardHome() {
  const [events, setEvents] = useState<string[]>([]);

  useEffect(() => {
    const stream = new EventSource("/stream/ops");

    stream.onmessage = (e) => {
      setEvents((prev) => [...prev.slice(-200), e.data]);
    };

    stream.onerror = () => stream.close();
    return () => stream.close();
  }, []);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Operational Metrics</h1>

      <div className="bg-black text-green-400 p-4 rounded max-h-80 overflow-auto text-sm">
        {events.map((line, i) => (
          <div key={i}>{line}</div>
        ))}
      </div>
    </div>
  );
}
