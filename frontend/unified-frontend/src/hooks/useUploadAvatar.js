// /src/hooks/useUploadAvatar.js
// SentinelOps — Upload Avatar Hook (Corrected Endpoint)

import { useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "../api/apiClient";

export default function useUploadAvatar() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload) => {
      let formData;

      if (payload instanceof FormData) {
        formData = payload;
      } else {
        formData = new FormData();
        formData.append("avatar", payload);
      }

      // ⭐ FIXED: correct backend endpoint
      const res = await apiClient.post("/users/me/avatar", formData, {
        withCredentials: true,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      return res.data;
    },

    onSuccess: () => {
      // Refresh authenticated profile so avatar_url updates
      queryClient.invalidateQueries({ queryKey: ["auth", "me"] });
    },
  });
}
