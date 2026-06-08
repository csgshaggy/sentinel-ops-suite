// src/api/profileApi.js
import axios from "axios";

/**
 * Base API URL:
 * - If Vite env is set, use it
 * - Otherwise fall back to same-origin
 */
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || window.location.origin;

/**
 * Axios instance that always sends cookies/session_id
 */
export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

/**
 * Convert backend avatar paths into fully usable URLs.
 *
 * Handles:
 * - S3/CDN absolute URLs:
 *   https://bucket.s3.amazonaws.com/avatars/x.png
 * - Local absolute URLs:
 *   https://crcybercop.dpdns.org/uploads/avatars/x.png
 * - Local relative URLs:
 *   /uploads/avatars/x.png
 *   uploads/avatars/x.png
 */
export function resolveAvatarUrl(url) {
  if (!url) return "/default-avatar.png";

  // Already absolute (S3, CDN, fully-qualified backend URL)
  if (/^https?:\/\//i.test(url)) {
    return url;
  }

  // Relative path from backend
  const normalized = url.startsWith("/") ? url : `/${url}`;
  return `${API_BASE_URL}${normalized}`;
}

/**
 * Add a cache-busting query param so the browser loads the fresh avatar.
 */
export function addCacheBust(url, version) {
  if (!url) return url;

  const separator = url.includes("?") ? "&" : "?";
  const v = version || Date.now();

  return `${url}${separator}v=${encodeURIComponent(v)}`;
}

/**
 * Normalize user object coming from backend so UI always gets a valid avatar URL.
 */
export function normalizeUser(user) {
  if (!user) return user;

  const rawAvatar =
    user.avatar_url || user.avatarThumbUrl || user.avatar_thumb_url || null;

  return {
    ...user,
    avatar_url: addCacheBust(resolveAvatarUrl(rawAvatar), user.avatar_version),
  };
}

export async function fetchCurrentUser() {
  const { data } = await api.get("/api/users/me");
  return normalizeUser(data);
}

/**
 * Upload avatar with progress callback.
 */
export async function uploadUserAvatar(file, onProgress) {
  const formData = new FormData();
  formData.append("avatar", file);

  const { data } = await api.post("/api/users/me/avatar", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress: (event) => {
      if (!event.total) return;
      const percent = Math.round((event.loaded * 100) / event.total);
      if (typeof onProgress === "function") {
        onProgress(percent);
      }
    },
  });

  /**
   * Backend currently returns:
   * { avatar_url: "..." }
   *
   * We normalize it here just in case.
   */
  return {
    ...data,
    avatar_url: addCacheBust(resolveAvatarUrl(data.avatar_url)),
  };
}
``
