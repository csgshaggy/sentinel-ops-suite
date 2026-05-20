import { useMutation } from "@tanstack/react-query";

interface EnrollResponse {
  qr_code: string;
  secret: string;
}

export function useEnrollMfa() {
  const token = localStorage.getItem("access_token");

  return useMutation<EnrollResponse>({
    mutationFn: async () => {
      const res = await fetch("/api/mfa/enroll", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) throw new Error("Failed to start MFA enrollment");
      return res.json();
    },
  });
}
