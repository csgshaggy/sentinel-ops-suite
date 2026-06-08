import { useRef, useState, useEffect, useMemo } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "../../../../api/apiClient";
import useAvatarUrl from "../../../../hooks/useAvatarUrl";

import AvatarCropModal from "../AvatarCropModal";
import { toast } from "../../../../components/ToastManager.jsx";

import "./AvatarTab.css";

const MAX_FILE_SIZE_MB = 5;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

const ALLOWED_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp"];
const ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"];

/* ------------------------------------------------------------
   Helpers
------------------------------------------------------------ */
function getApiBaseUrl() {
  const configuredBase = apiClient?.defaults?.baseURL || "";
  return configuredBase.replace(/\/+$/, "");
}

function resolveAvatarUrl(url) {
  if (!url) return null;

  // Already absolute (S3/CDN/full backend URL)
  if (/^https?:\/\//i.test(url)) {
    return url;
  }

  // Relative local path
  const normalized = url.startsWith("/") ? url : `/${url}`;
  const base = getApiBaseUrl();

  return base ? `${base}${normalized}` : normalized;
}

function addCacheBust(url, version) {
  if (!url) return url;
  const separator = url.includes("?") ? "&" : "?";
  const v = version || Date.now();
  return `${url}${separator}v=${encodeURIComponent(v)}`;
}

function normalizeAvatarUrl(url, version) {
  const resolved = resolveAvatarUrl(url);
  return resolved ? addCacheBust(resolved, version) : null;
}

function hasAllowedExtension(filename = "") {
  const lower = filename.toLowerCase();
  return ALLOWED_EXTENSIONS.some((ext) => lower.endsWith(ext));
}

export default function AvatarTab({ profile, refetchProfile }) {
  const queryClient = useQueryClient();

  const fileInputRef = useRef(null);
  const tempObjectUrlRef = useRef(null);

  /**
   * Keep your existing hook as a fallback in case it already handles
   * app-specific avatar resolution logic.
   */
  const hookAvatarUrl = useAvatarUrl(profile);

  const incomingAvatarUrl = useMemo(() => {
    return normalizeAvatarUrl(
      profile?.avatar_thumb_url || profile?.avatar_url || hookAvatarUrl,
      profile?.avatar_version
    );
  }, [
    profile?.avatar_thumb_url,
    profile?.avatar_url,
    profile?.avatar_version,
    hookAvatarUrl,
  ]);

  const [preview, setPreview] = useState(incomingAvatarUrl || null);
  const [originalAvatar, setOriginalAvatar] = useState(incomingAvatarUrl || null);
  const [error, setError] = useState(null);

  const [pendingImage, setPendingImage] = useState(null);
  const [pendingUploadBlob, setPendingUploadBlob] = useState(null);
  const [hasNewUpload, setHasNewUpload] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const revokeTempObjectUrl = () => {
    if (tempObjectUrlRef.current) {
      URL.revokeObjectURL(tempObjectUrlRef.current);
      tempObjectUrlRef.current = null;
    }
  };

  useEffect(() => {
    return () => revokeTempObjectUrl();
  }, []);

  /**
   * Keep preview synced with backend profile unless the user has an unsaved crop.
   */
  useEffect(() => {
    if (hasNewUpload) return;

    revokeTempObjectUrl();
    setPreview(incomingAvatarUrl || null);
    setOriginalAvatar(incomingAvatarUrl || null);
    setPendingUploadBlob(null);
    setPendingImage(null);
    setError(null);
    setUploadProgress(0);
  }, [incomingAvatarUrl, hasNewUpload]);

  /* ------------------------------------------------------------
     Upload mutation
     - POST /users/me/avatar
     - Tracks upload progress
     - Updates React Query cache
     - Invalidates profile query to re-fetch authoritative data
  ------------------------------------------------------------ */
  const uploadAvatarMutation = useMutation({
    mutationFn: async (blob) => {
      const formData = new FormData();
      formData.append("avatar", blob, "avatar-upload.webp");

      const response = await apiClient.post("/users/me/avatar", formData, {
        withCredentials: true,
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (event) => {
          if (!event?.total) return;
          const percent = Math.round((event.loaded * 100) / event.total);
          setUploadProgress(percent);
        },
      });

      return response.data;
    },

    onSuccess: async (result) => {
      const freshAvatarUrl = normalizeAvatarUrl(
        result?.avatar_url || originalAvatar,
        Date.now()
      );

      revokeTempObjectUrl();

      setOriginalAvatar(freshAvatarUrl);
      setPreview(freshAvatarUrl);
      setPendingUploadBlob(null);
      setHasNewUpload(false);
      setError(null);
      setUploadProgress(100);

      // Optimistically update the cached profile immediately
      queryClient.setQueryData(["profile"], (oldProfile) => {
        if (!oldProfile) return oldProfile;

        return {
          ...oldProfile,
          avatar_url: freshAvatarUrl,
          avatar_thumb_url: freshAvatarUrl,
          avatar_version: Date.now(),
        };
      });

      // Re-fetch authoritative profile from backend
      await queryClient.invalidateQueries({
        queryKey: ["profile"],
      });

      // Optional compatibility if parent still passes a manual refetch
      if (typeof refetchProfile === "function") {
        await Promise.resolve(refetchProfile());
      }

      if (toast?.success) {
        toast.success("Avatar updated successfully.");
      }
    },

    onError: (err) => {
      const message =
        err?.response?.data?.detail ||
        err?.message ||
        "Unable to upload avatar.";

      setError(message);

      if (toast?.error) {
        toast.error(message);
      }
    },

    onSettled: () => {
      setTimeout(() => {
        setUploadProgress(0);
      }, 600);
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
      if (toast?.error) toast.error(message);
      e.target.value = "";
      return;
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      const message = `Avatar must be ${MAX_FILE_SIZE_MB}MB or smaller.`;
      setError(message);
      if (toast?.error) toast.error(message);
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
    if (!pendingUploadBlob || uploadAvatarMutation.isPending) return;
    await uploadAvatarMutation.mutateAsync(pendingUploadBlob);
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

  const isUploading = uploadAvatarMutation.isPending;

  return (
    <div className="avatar-tab-container">
      <h2>Avatar</h2>

      <div className="avatar-panel">
        <div className="avatar-preview-wrapper">
          {preview ? (
            {preview}
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
