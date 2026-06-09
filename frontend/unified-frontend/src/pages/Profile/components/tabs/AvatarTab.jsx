// src/pages/Profile/components/tabs/AvatarTab.jsx

import { useRef, useState, useEffect, useMemo } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import apiClient from "../../../../api/apiClient";
import useAvatarUrl from "../../../../hooks/useAvatarUrl";
import AvatarCropModal from "../AvatarCropModal";
import { toast } from "../../../../components/ToastManager.jsx";

import "./AvatarTab.css";

/* ------------------------------------------------------------
   Constants
------------------------------------------------------------ */
const MAX_FILE_SIZE_MB = 5;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

const ALLOWED_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp"];
const ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"];

/* ------------------------------------------------------------
   Helpers
------------------------------------------------------------ */
function hasAllowedExtension(filename = "") {
  const lower = filename.toLowerCase();
  return ALLOWED_EXTENSIONS.some((ext) => lower.endsWith(ext));
}

export default function AvatarTab({ profile }) {
  const queryClient = useQueryClient();

  const fileInputRef = useRef(null);
  const tempObjectUrlRef = useRef(null);

  const hookAvatarUrl = useAvatarUrl(profile);

  const incomingAvatarUrl = useMemo(() => {
    return (
      hookAvatarUrl ||
      profile?.avatar_thumb_url ||
      profile?.avatar_url ||
      null
    );
  }, [profile?.avatar_thumb_url, profile?.avatar_url, hookAvatarUrl]);

  const [preview, setPreview] = useState(incomingAvatarUrl);
  const [originalAvatar, setOriginalAvatar] = useState(incomingAvatarUrl);

  const [pendingImage, setPendingImage] = useState(null);
  const [pendingUploadBlob, setPendingUploadBlob] = useState(null);

  const [hasNewUpload, setHasNewUpload] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);

  const revokeTempObjectUrl = () => {
    if (tempObjectUrlRef.current) {
      URL.revokeObjectURL(tempObjectUrlRef.current);
      tempObjectUrlRef.current = null;
    }
  };

  useEffect(() => {
    return () => revokeTempObjectUrl();
  }, []);

  useEffect(() => {
    if (hasNewUpload) return;

    revokeTempObjectUrl();
    setPreview(incomingAvatarUrl);
    setOriginalAvatar(incomingAvatarUrl);
    setPendingUploadBlob(null);
    setPendingImage(null);
    setError(null);
    setUploadProgress(0);
  }, [incomingAvatarUrl, hasNewUpload]);

  /* ------------------------------------------------------------
     Upload Mutation (Unified, aligned with backend)
------------------------------------------------------------ */
  const uploadMutation = useMutation({
    mutationFn: async (blob) => {
      const formData = new FormData();
      // ⭐ Field name MUST match FastAPI UploadFile parameter (e.g. avatar: UploadFile = File(...))
      formData.append("avatar", blob, "avatar.png");

      const res = await apiClient.post("/api/users/me/avatar", formData, {
        withCredentials: true,
        // Let the browser set the multipart boundary
      });

      return res.data;
    },

    onSuccess: async (result) => {
      const freshUrl = result?.avatar_thumb_url || result?.avatar_url;

      revokeTempObjectUrl();

      setOriginalAvatar(freshUrl);
      setPreview(freshUrl);
      setPendingUploadBlob(null);
      setHasNewUpload(false);
      setError(null);
      setUploadProgress(100);

      // Optimistic update
      queryClient.setQueryData(["profile"], (old) => {
        if (!old) return old;
        return {
          ...old,
          avatar_url: freshUrl,
          avatar_thumb_url: freshUrl,
          avatar_version: result?.avatar_version,
        };
      });

      await queryClient.invalidateQueries({ queryKey: ["profile"] });

      toast?.success?.("Avatar updated successfully.");
    },

    onError: (err) => {
      const message =
        err?.response?.data?.detail ||
        err?.message ||
        "Unable to upload avatar.";

      setError(message);
      toast?.error?.(message);
    },

    onSettled: () => {
      setTimeout(() => setUploadProgress(0), 600);
    },
  });

  /* ------------------------------------------------------------
     Handlers
------------------------------------------------------------ */
  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setError(null);

    if (!ALLOWED_TYPES.includes(file.type) || !hasAllowedExtension(file.name)) {
      const message = "Only PNG, JPG, JPEG, and WEBP images are allowed.";
      setError(message);
      toast?.error?.(message);
      e.target.value = "";
      return;
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      const message = `Avatar must be ${MAX_FILE_SIZE_MB}MB or smaller.`;
      setError(message);
      toast?.error?.(message);
      e.target.value = "";
      return;
    }

    setPendingImage(file);
    e.target.value = "";
  };

  const handleCroppedSave = (blob) => {
    revokeTempObjectUrl();

    const objectUrl = URL.createObjectURL(blob);
    tempObjectUrlRef.current = objectUrl;

    setPreview(objectUrl);
    setPendingUploadBlob(blob);
    setPendingImage(null);
    setHasNewUpload(true);
    setError(null);
  };

  const handleSaveAvatar = async () => {
    if (!pendingUploadBlob || uploadMutation.isPending) return;
    await uploadMutation.mutateAsync(pendingUploadBlob);
  };

  const handleRevertChanges = () => {
    revokeTempObjectUrl();
    setPreview(originalAvatar);
    setPendingUploadBlob(null);
    setPendingImage(null);
    setHasNewUpload(false);
    setError(null);
    setUploadProgress(0);
  };

  const isUploading = uploadMutation.isPending;

  /* ------------------------------------------------------------
     Render
------------------------------------------------------------ */
  return (
    <div className="avatar-tab-container">
      <h2>Avatar</h2>

      <div className="avatar-panel">
        <div className="avatar-preview-wrapper">
          {preview ? (
            <img src={preview} alt="Avatar preview" className="avatar-preview" />
          ) : (
            <div>No avatar</div>
          )}
        </div>

        <button
          className="avatar-btn"
          type="button"
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
        >
          {isUploading ? "Uploading..." : "Upload New Avatar"}
        </button>

        <input
          ref={fileInputRef}
          type="file"
          accept={ALLOWED_EXTENSIONS.join(",")}
          style={{ display: "none" }}
          onChange={handleFileChange}
        />

        <div className="avatar-actions">
          <button
            className="avatar-btn"
            type="button"
            disabled={!hasNewUpload || isUploading}
            onClick={handleSaveAvatar}
          >
            {isUploading ? "Saving..." : "Save Avatar"}
          </button>

          <button
            className="avatar-btn"
            type="button"
            disabled={!hasNewUpload || isUploading}
            onClick={handleRevertChanges}
          >
            Revert Changes
          </button>
        </div>

        {isUploading && (
          <div className="upload-progress-wrapper" aria-live="polite">
            <div className="upload-progress-bar">
              <div
                className="upload-progress-fill"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
            <div className="upload-progress-text">{uploadProgress}%</div>
          </div>
        )}

        {error && <div className="profile-error">{error}</div>}
      </div>

      {pendingImage && (
        <AvatarCropModal
          image={pendingImage}
          onClose={() => setPendingImage(null)}
          onSave={handleCroppedSave}
        />
      )}
    </div>
  );
}
