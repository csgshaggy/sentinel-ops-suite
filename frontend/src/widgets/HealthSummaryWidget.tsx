import React, { useEffect, useState } from "react";

import { fetchMakefileHealth, fetchPlugins, fetchTimingBuckets } from "../api/client";

export default function HealthSummaryWidget() {
  const [makefileHealth, setMakefileHealth] = useState(100);
  const [pluginHealth, setPluginHealth] = useState(100);
  const [timingHealth, setTimingHealth] = useState(100);

  useEffect(() => {
    const load = async () => {
      const mf = await fetchMakefileHealth();
      setMakefileHealth(mf.health);

      const plugins = await fetchPlugins();
      const ok = plugins.filter((p) => p.status === "ok").length;
      const pct = Math.round((ok / plugins.length) * 100);
      setPluginHealth(pct);

      const timing = await fetchTimingBuckets();
      const total = timing.reduce((a, b) => a + b.count, 0);
      const fast = timing.filter((b) => b.bucket.includes("0-50")).reduce((a, b) => a + b.count, 0);
      setTimingHealth(Math.round((fast / total) * 100));
    };

    load();
  }, []);

  return (
    <div
      style={{
        padding: "1rem",
        background: "var(--bg-panel)",
        border: "1px solid var(--border)",
        borderRadius: "6px",
        marginBottom: "1rem",
      }}
    >
      <h3>System Health Summary</h3>

      <p>
        <strong>Makefile Health:</strong> {makefileHealth}
      </p>
      <p>
        <strong>Plugin Health:</strong> {pluginHealth}
      </p>
      <p>
        <strong>Timing Health:</strong> {timingHealth}
      </p>

      <h2 style={{ marginTop: "1rem" }}>
        Overall Score: {Math.round((makefileHealth + pluginHealth + timingHealth) / 3)}
      </h2>
    </div>
  );
}
