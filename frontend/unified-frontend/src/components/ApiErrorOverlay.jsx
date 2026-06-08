// /src/components/ApiErrorOverlay.jsx

import { useEffect, useState } from "react";
import { subscribeApiError } from "./apiErrorBus.js";

export default function ApiErrorOverlay() {
  const [error, setError] = useState(null);

  useEffect(() => {
    const unsub = subscribeApiError((payload) => {
      setError({
        message: payload.message,
        type: payload.type,
      });

      // Auto-clear after 6 seconds
      setTimeout(() => setError(null), 6000);
    });

    return () => unsub();
  }, []);

  if (!error) return null;

  return (
    <div
      style={{
        position: "fixed",
        bottom: "20px",
        right: "20px",
        padding: "1rem 1.5rem",
        background: "rgba(255, 0, 0, 0.85)",
        color: "white",
        borderRadius: "8px",
        zIndex: 9999,
        fontWeight: "bold",
        boxShadow: "0 0 12px rgba(0,0,0,0.4)",
      }}
    >
      {error.message}
    </div>
  );
}
