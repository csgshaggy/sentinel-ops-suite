import React, { useEffect } from "react";

import { notify } from "./NotificationCenter";

export default function OpsAlerts() {
  useEffect(() => {
    const stream = new EventSource("/stream/ops");

    stream.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);

        if (data.type === "anomaly" && data.score > 80) {
          notify(`High anomaly score: ${data.score}`, "error");
        }

        if (data.type === "idrim" && data.drift === "high") {
          notify("IDRIM: High IAM drift detected", "error");
        }

        if (data.type === "pelm" && data.risk >= 4) {
          notify(`PELM risk level: ${data.risk}`, "warning" as any);
        }
      } catch {
        // ignore malformed events
      }
    };

    stream.onerror = () => stream.close();
    return () => stream.close();
  }, []);

  return null;
}
