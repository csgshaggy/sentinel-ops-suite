import { useState } from "react";

export function useMfaDisable() {
  const [loading, setLoading] = useState(false);
  const [disabled, setDisabled] = useState(false);

  async function disable() {
    setLoading(true);
    try {
      const res = await fetch("/api/mfa/disable", { method: "POST" });
      if (res.ok) setDisabled(true);
      return res.ok;
    } finally {
      setLoading(false);
    }
  }

  return { disable, loading, disabled };
}
