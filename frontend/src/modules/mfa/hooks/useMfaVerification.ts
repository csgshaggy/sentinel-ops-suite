import { useState } from "react";

export function useMfaVerification() {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState<boolean | null>(null);

  async function verify(code: string) {
    setLoading(true);
    try {
      const res = await fetch("/api/mfa/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      setSuccess(res.ok);
      return res.ok;
    } finally {
      setLoading(false);
    }
  }

  return { verify, loading, success };
}
