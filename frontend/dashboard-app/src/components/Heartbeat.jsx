import React, { useEffect, useState } from "react";

export default function Heartbeat() {
  const [status, setStatus] = useState("unknown"); 
  // "ok" | "slow" | "down" | "unknown"

  useEffect(() => {
    const checkHeartbeat = async () => {
      const start = performance.now();

      try {
        const res = await fetch("/api/heartbeat", {
          method: "GET",
          credentials: "include",
        });

        const latency = performance.now() - start;

        if (!res.ok) {
          setStatus("down");
          return;
        }

        if (latency < 300) setStatus("ok");
        else if (latency < 1200) setStatus("slow");
        else setStatus("down");

      } catch (err) {
        setStatus("down");
      }
    };

    // Initial check
    checkHeartbeat();

    // Poll every 5 seconds
    const interval = setInterval(checkHeartbeat, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      className={`heartbeat-dot heartbeat-${status}`}
      title={`Backend status: ${status}`}
    ></div>
  );
}
