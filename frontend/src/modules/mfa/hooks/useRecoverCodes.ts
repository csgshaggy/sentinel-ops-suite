import { useState } from "react";

export function useRecoveryCodes() {
  const [codes, setCodes] = useState<string[] | null>(null);
  const [loading, setLoading] = useState(false);

  async function loadCodes() {
    setLoading(true);
    try {
      const res = await fetch("/api/mfa/recovery-codes");
      const json = await res.json();
      setCodes(json.codes);
    } finally {
      setLoading(false);
    }
  }

  async function regenerate() {
    setLoading(true);
    try {
      const res = await fetch("/api/mfa/recovery-codes/regenerate", {
        method: "POST",
      });
      const json = await res.json();
      setCodes(json.codes);
    } finally {
      setLoading(false);
    }
  }

  return { codes, loading, loadCodes, regenerate };
}
