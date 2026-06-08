``
import { useRef, useState, useEffect } from "react";
import useUploadAvatar from "../../../../hooks/useUploadAvatar";
import useAvatarUrl from "../../../../hooks/useAvatarUrl";

import AvatarCropModal from "../AvatarCropModal";
import { toast } from "../../../../components/ToastManager.jsx";

import "./AvatarTab.css";

const MAX_FILE_SIZE_MB = 5;
const ALLOWED_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp"];
const ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"];

export default function AvatarTab({ profile, refetchProfile }) {
  const fileInputRef = useRef(null);
  const tempObjectUrlRef = useRef(null);

  const uploadAvatar = useUploadAvatar();
  const avatarUrl = useAvatarUrl(profile);

  const [preview, setPreview] = useState(avatarUrl || null);
  const [originalAvatar, setOriginalAvatar] = useState(avatarUrl || null);
  const [error, setError] = useState(null);

  const [pendingImage, setPendingImage] = useState(null);
  const [pendingUploadBlob, setPendingUploadBlob] = useState(null);
  const [hasNewUpload, setHasNewUpload] = useState(false);
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [showResetConfirm, setShowResetConfirm] = useState(false);

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
    setPreview(avatarUrl || null);
    setOriginalAvatar(avatarUrl || null);
    setPendingUploadBlob(null);
    setPendingImage(null);
    setError(null);
  }, [avatarUrl, hasNewUpload]);

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setPendingImage(file);
    e.target.value = "";
  };

  const handleCroppedSave = (blob) => {
    revokeTempObjectUrl();
    const url = URL.createObjectURL(blob);
    tempObjectUrlRef.current = url;

    setPreview(url);
    setPendingUploadBlob(blob);
    setHasNewUpload(true);
  };

  const handleSaveAvatar = async () => {
    if (!pendingUploadBlob) return;

    const formData = new FormData();
    formData.append("avatar", pendingUploadBlob);

    const result = await uploadAvatar.mutateAsync(formData);
    const nextUrl = result?.avatar_url || originalAvatar;

    revokeTempObjectUrl();

    setOriginalAvatar(nextUrl);
    setPreview(nextUrl);
    setPendingUploadBlob(null);
    setHasNewUpload(false);
  };

  return (
    <div className="avatar-tab-container">
      <h2>Avatar</h2>

      <div className="avatar-panel">
        <div className="avatar-preview-wrapper">
          {preview ? (
            <img src={preview} className="avatar-preview" />
          ) : (
            <div>No avatar</div>
          )}
        </div>

        <button
          className="avatar-btn"
          onClick={() => fileInputRef.current?.click()}
        >
          Upload New Avatar
        </button>

        <input
          ref={fileInputRef}
          type="file"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />

        <div className="avatar-actions">
          <button
            className="avatar-btn"
            disabled={!hasNewUpload}
            onClick={handleSaveAvatar}
          >
            Save Avatar
          </button>

          <button
            className="avatar-btn"
            disabled={!hasNewUpload}
            onClick={() => {
              revokeTempObjectUrl();
              setPreview(originalAvatar);
              setHasNewUpload(false);
              setPendingUploadBlob(null);
            }}
          >
            Revert Changes
          </button>
        </div>
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
