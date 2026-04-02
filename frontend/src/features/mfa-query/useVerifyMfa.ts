import { useMutation } from "@tanstack/react-query";

export function useVerifyMfa() {
  const token = localStorage.getItem("access_token");

  return useMutation({
    mutationFn: async (code: string) => {
      const res = await fetch("/api/mfa/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ code }),
      });

      if (!res.ok) throw new Error("Verification failed");
      return res.json();
    },
  });
}
