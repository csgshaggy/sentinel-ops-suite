import { useEffect, useState } from "react";

export function useSessionExpiry() {
  const [expiresIn, setExpiresIn] = useState<number | null>(null);

  useEffect(() => {
    const expiry = localStorage.getItem("session_expiry");
    if (!expiry) return;

    const update = () => {
      const remaining = Number(expiry) - Date.now();
      setExpiresIn(remaining > 0 ? remaining : 0);
    };

    update();
    const interval = setInterval(update, 1000);

    return () => clearInterval(interval);
  }, []);

  return expiresIn;
}
