// /src/components/profile/AvatarUploader.jsx
// SentinelOps — Avatar Uploader (Unified + Cache‑Safe + React‑18 Safe)

import React, { useState, useEffect } from "react";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

export default function AvatarUploader({ avatarUrl, onUploaded }) {
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);

  // ------------------------------------------------------------
  // Sync preview with server avatar (cache‑busted)
  // ------------------------------------------------------------
  useEffect(() => {
    if (avatarUrl) {
      setPreview(`${avatarUrl}?t=${Date.now()}`);
    }
  }, [avatarUrl]);

  // ------------------------------------------------------------
  // Cleanup blob URLs on unmount
  // ------------------------------------------------------------
  useEffect(() => {
    return () => {
      if (preview && preview.startsWith("blob:")) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  // ------------------------------------------------------------
  // Handle avatar upload
  // ------------------------------------------------------------
  const handleFile = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Local preview
    const localUrl = URL.createObjectURL(file);
    setPreview(localUrl);

    const formData = new FormData();
    formData.append("avatar", file);

    try {
      setUploading(true);

      const res = await apiClient.post("/profile/avatar", formData, {
        withCredentials: true,
      });

      if (!res.ok) {
        toast.error("Failed to upload avatar.");
        return;
      }

      const serverUrl = res.data.avatar_url;
      const bustedUrl = `${serverUrl}?t=${Date.now()}`;

      setPreview(bustedUrl);
      onUploaded?.(bustedUrl);

      toast.success("Avatar updated successfully.");
    } catch (err) {
      console.error("Avatar upload failed:", err);
      toast.error("Failed to upload avatar.");
    } finally {
      setUploading(false);
    }
  };

  // ------------------------------------------------------------
  // Fallback avatar
  // ------------------------------------------------------------
  const fallbackAvatar = "/static/avatars/default-avatar.png";

  return (
    <div className="avatar-upload-container">
      <img
        src={preview || fallbackAvatar}
        alt="Avatar Preview"
        className="avatar-preview"
      />

      <label className="profile-button" style={{ marginTop: "12px" }}>
        {uploading ? "Uploading..." : "Upload New Avatar"}
        <input
          type="file"
          accept="image/png, image/jpeg"
          style={{ display: "none" }}
          onChange={handleFile}
        />
      </label>
    </div>
  );
}

