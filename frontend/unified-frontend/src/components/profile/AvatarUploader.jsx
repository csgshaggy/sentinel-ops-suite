// /src/components/profile/AvatarUploader.jsx

import React, { useState, useEffect } from "react";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

export default function AvatarUploader({ avatarUrl, onUploaded }) {
  const [preview, setPreview] = useState(avatarUrl || null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (avatarUrl) {
      setPreview(`${avatarUrl}?t=${Date.now()}`);
    }
  }, [avatarUrl]);

  useEffect(() => {
    return () => {
      if (preview && preview.startsWith("blob:")) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  const handleFile = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const localUrl = URL.createObjectURL(file);
    setPreview(localUrl);

    const formData = new FormData();
    formData.append("avatar", file);

    try {
      setUploading(true);

      // ⭐ FIXED: send cookies + let axios set Content-Type automatically
      const res = await apiClient.post("/api/auth/profile/avatar", formData, {
        withCredentials: true,
      });

      const serverUrl = res.data.avatar_url;
      const bustedUrl = `${serverUrl}?t=${Date.now()}`;

      setPreview(bustedUrl);

      if (onUploaded) onUploaded(bustedUrl);

      toast.success("Avatar updated successfully.");
    } catch (err) {
      console.error("Avatar upload failed:", err);
      toast.error("Failed to upload avatar.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="avatar-upload-container">
      <img
        src={preview || "/default-avatar.png"}
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
