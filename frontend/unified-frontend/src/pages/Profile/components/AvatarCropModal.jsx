// /src/pages/Profile/components/AvatarCropModal.jsx
// SentinelOps — Avatar Crop Modal (React Easy Crop + Neon‑Glassy)

import { useEffect, useState, useCallback } from "react";
import Cropper from "react-easy-crop";
import { createThumbnailFromFile } from "./utils/ThumbnailService";

import "./AvatarCropModal.css";

export default function AvatarCropModal({ image, onClose, onSave }) {
  const [imageSrc, setImageSrc] = useState(null);
  const [previewKey, setPreviewKey] = useState(Date.now());
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);
  const [saving, setSaving] = useState(false);

  // ------------------------------------------------------------
  // Convert File → DataURL (preview source)
  // ------------------------------------------------------------
  useEffect(() => {
    if (!image) return;

    const reader = new FileReader();
    reader.onload = () => {
      setImageSrc(reader.result);
      setPreviewKey(Date.now()); // still useful for internal refresh logic
    };
    reader.readAsDataURL(image);
  }, [image]);

  // ------------------------------------------------------------
  // React Easy Crop callback
  // ------------------------------------------------------------
  const onCropComplete = useCallback((_, croppedPixels) => {
    setCroppedAreaPixels(croppedPixels);
  }, []);

  // ------------------------------------------------------------
  // Save cropped avatar
  // ------------------------------------------------------------
  const handleSave = async () => {
    if (!imageSrc || !croppedAreaPixels) return;

    setSaving(true);

    try {
      // Generate 256×256 cropped blob
      const { blob } = await createThumbnailFromFile(
        imageSrc,
        croppedAreaPixels,
        256,
        256
      );

      await onSave(blob);
    } finally {
      setSaving(false);
    }
  };

  if (!imageSrc) return null;

  return (
    <div className="avatar-crop-modal-overlay">
      <div className="avatar-crop-modal glass">
        <h2 className="avatar-crop-title">Crop Avatar</h2>

        {/* Cropper */}
        <div className="avatar-crop-preview">
          <div
            style={{
              position: "relative",
              width: "100%",
              height: "260px",
              background: "#020617",
              borderRadius: "12px",
              overflow: "hidden",
            }}
          >
            <Cropper
              image={imageSrc}   // ← FIXED: no ?t= on DataURLs
              crop={crop}
              zoom={zoom}
              aspect={1}
              cropShape="round"
              showGrid={false}
              onCropChange={setCrop}
              onZoomChange={setZoom}
              onCropComplete={onCropComplete}
            />
          </div>
        </div>

        {/* Zoom slider + actions */}
        <div className="avatar-crop-actions">
          <label style={{ flex: 1, marginRight: "12px", color: "#9fb3c8" }}>
            Zoom
            <input
              type="range"
              min={1}
              max={3}
              step={0.1}
              value={zoom}
              onChange={(e) => setZoom(Number(e.target.value))}
              style={{ width: "100%" }}
            />
          </label>

          <button
            className="btn-secondary"
            onClick={onClose}
            disabled={saving}
          >
            Cancel
          </button>

          <button
            className="btn-primary"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? "Saving…" : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
}
