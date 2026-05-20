import { useState } from "react";

interface EnrollmentData {
  qrImageUrl: string;
  secret: string;
}

export function useMfaEnrollment() {
  const [data, setData] = useState<EnrollmentData | null>(null);
  const [loading, setLoading] = useState(false);

  async function startEnrollment() {
    setLoading(true);
    try {
      const res = await fetch("/api/mfa/enroll/start");
      const json = await res.json();
      setData(json);
    } finally {
      setLoading(false);
    }
  }

  return { data, loading, startEnrollment };
}
