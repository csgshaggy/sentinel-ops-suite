// frontend/src/api/profileClient.js
// Unified Profile + Avatar API Client

import apiClient from "./apiClient";

/* ------------------------------------------------------------
   GET /api/users/me
------------------------------------------------------------ */
export async function fetchProfile() {
  const res = await apiClient.get("/users/me", {
    withCredentials: true,
  });
  return res.data;
}

/* ------------------------------------------------------------
   POST /api/users/me/avatar
   - Backend expects field name: "file"
   - Must be multipart/form-data
------------------------------------------------------------ */
export async function uploadAvatar(file, onProgress) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await apiClient.post("/users/me/avatar", formData, {
    withCredentials: true,
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress: (event) => {
      if (onProgress && event?.total) {
        const percent = Math.round((event.loaded * 100) / event.total);
        onProgress(percent);
      }
    },
  });

  return res.data;
}
