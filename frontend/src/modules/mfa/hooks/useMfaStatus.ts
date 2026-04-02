import { useEffect, useState } from "react";

interface MfaStatus {
  enabled: boolean;
  methods: string[];
}

export function useMfaStatus() {
  const [status, setStatus] = useState<MfaStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch("/api/mfa/status");
        const data = await res.json();
        setStatus(data);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return { status, loading };
}
