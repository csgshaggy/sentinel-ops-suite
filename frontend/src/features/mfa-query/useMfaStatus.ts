import { useQuery } from "@tanstack/react-query";

interface MfaStatusResponse {
  enabled: boolean;
}

export function useMfaStatus() {
  const token = localStorage.getItem("access_token");

  return useQuery<MfaStatusResponse>({
    queryKey: ["mfa-status"],
    queryFn: async () => {
      const res = await fetch("/api/mfa/status", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) throw new Error("Failed to fetch MFA status");
      return res.json();
    },
  });
}
