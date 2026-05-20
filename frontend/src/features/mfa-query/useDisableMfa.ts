import { useMutation } from "@tanstack/react-query";

export function useDisableMfa() {
  const token = localStorage.getItem("access_token");

  return useMutation({
    mutationFn: async () => {
      const res = await fetch("/api/mfa/disable", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) throw new Error("Failed to disable MFA");
      return res.json();
    },
  });
}
