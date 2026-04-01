import React, { useEffect, useState } from "react";

export default function PelmDashboard() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch("/pelm/health")
      .then((res) => res.json())
      .then((data) => setHealth(data))
      .catch(() => setHealth({ status: "error" }));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>PELM Module</h1>
      <pre>{JSON.stringify(health, null, 2)}</pre>
    </div>
  );
}
