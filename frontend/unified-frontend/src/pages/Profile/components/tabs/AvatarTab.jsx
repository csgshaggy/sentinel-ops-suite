import { useRef, useState, useEffect } from "react";
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

function getApiBaseUrl() {
  const configuredBase = apiClient?.defaults?.baseURL || "";
  return configuredBase.replace(/\/+$/, "");
}

function resolveAvatarUrl(url) {
  if (!url) return "/default-avatar.png";

  // S3/CDN/full backend URL
  if (/^https?:\/\//i.test(url)) {
    return url;
  }

  // Relative local URL
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
  return addCacheBust(resolveAvatarUrl(url), version);
}

function hasAllowedExtension(filename = "") {
  const lower = filename.toLowerCase();
  return ALLOWED_EXTENSIONS.some((ext) => lower.endsWith(ext));
}

export default function AvatarTab({ profile, refetchProfile }) {
  const queryClient = useQueryClient();

  const fileInputRef = useRef(null);
  const tempObjectUrlRef = useRef(null);

  const hookAvatarUrl = useAvatarUrl(profile);
  const initialAvatarUrl = normalizeAvatarUrl(
    profile?.avatar_thumb_url || profile?.avatar_url || hookAvatarUrl,
    profile?.avatar_version
  );

  const [preview, setPreview] = useState(initialAvatarUrl || null);
  const [originalAvatar, setOriginalAvatar] = useState(initialAvatarUrl || null);
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

  useEffect(() => {
    if (hasNewUpload) return;

    const nextAvatar = normalizeAvatarUrl(
      profile?.avatar_thumb_url || profile?.avatar_url || hookAvatarUrl,
      profile?.avatar_version
    );

    revokeTempObjectUrl();
    setPreview(nextAvatar || null);
    setOriginalAvatar(nextAvatar || null);
    setPendingUploadBlob(null);
    setPendingImage(null);
    setError(null);
    setUploadProgress(0);
  }, [
    profile?.avatar_thumb_url,
    profile?.avatar_url,
    profile?.avatar_version,
    hookAvatarUrl,
    hasNewUpload,
  ]);

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
      const nextUrl = normalizeAvatarUrl(
        result?.avatar_url || originalAvatar,
        Date.now()
      );

      revokeTempObjectUrl();

      setOriginalAvatar(nextUrl);
      setPreview(nextUrl);
      setPendingUploadBlob(null);
      setHasNewUpload(false);
      setUploadProgress(100);
      setError(null);

      // Update any cached profile data immediately
      queryClient.setQueryData(["profile"], (oldProfile) => {
        if (!oldProfile) return oldProfile;

        return {
          ...oldProfile,
          avatar_url: nextUrl,
          avatar_thumb_url: nextUrl,
          avatar_version: Date.now(),
        };
      });

      // Re-fetch authoritative profile response
      await queryClient.invalidateQueries({
        queryKey: ["profile"],
      });

      // If parent passed an explicit refetch, run it too
      if (typeof refetchProfile === "function") {
        await Promise.resolve(refetchProfile());
      }

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
      setTimeout(() => {
        setUploadProgress(0);
      }, 600);
    },
  });

  const handleFileChange = async (e) => {
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

    const tempUrl = URL.createObjectURL(blob);
    tempObjectUrlRef.current = tempUrl;

    setPreview(tempUrl);
    setPendingUploadBlob(blob);
    setHasNewUpload(true);
    setPendingImage(null);
    setError(null);
  };

  const handleSaveAvatar = async () => {
    if (!pendingUploadBlob || uploadAvatarMutation.isPending) return;
    await uploadAvatarMutation.mutateAsync(pendingUploadBlob);
  };

  const handleRevertChanges = () => {
    revokeTempObjectUrl();
    setPreview(originalAvatar);
    setHasNewUpload(false);
    setPendingUploadBlob(null);
    setPendingImage(null);
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
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
          type="button"
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
            disabled={!hasNewUpload || isUploading}
            onClick={handleSaveAvatar}
            type="button"
          >
            {isUploading ? "Saving..." : "Save Avatar"}
          </button>

          <button
            className="avatar-btn"
            disabled={!hasNewUpload || isUploading}
            onClick={handleRevertChanges}
            type="button"
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
