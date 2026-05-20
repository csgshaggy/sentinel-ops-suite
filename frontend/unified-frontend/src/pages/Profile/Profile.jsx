// /src/pages/Profile/Profile.jsx

import { useState, useEffect, useCallback } from "react";
import apiClient from "../../api/apiClient.js";
import { toast } from "../../components/ToastManager.jsx";

import AvatarUploader from "../../components/profile/AvatarUploader.jsx";
import MFAToggle from "../../components/profile/MFAToggle.jsx";
import ChangePasswordForm from "../../components/profile/ChangePasswordForm.jsx";
import ProfileTabs from "../../components/profile/ProfileTabs.jsx";

import "./Profile.css";

export default function Profile() {
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);

  const [mfaQr, setMfaQr] = useState(null);
  const [mfaSecret, setMfaSecret] = useState(null);

  // ------------------------------------------------------------
  // Fetch profile (FIXED: send cookies)
  // ------------------------------------------------------------
  const fetchProfile = useCallback(async (signal) => {
    try {
      const res = await apiClient.get("/api/auth/profile", {
        signal,
        withCredentials: true,   // ⭐ REQUIRED
      });
      setProfile(res.data);
    } catch (err) {
      if (err.name === "CanceledError") return;
      console.error("Failed to load profile:", err);
      toast.error("Failed to load profile.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    Promise.resolve().then(() => fetchProfile(controller.signal));
    return () => controller.abort();
  }, [fetchProfile]);

  // ------------------------------------------------------------
  // Save profile changes (FIXED: send cookies)
  // ------------------------------------------------------------
  const handleSave = async () => {
    try {
      await apiClient.post(
        "/api/auth/profile/update",
        {
          email: profile.email,
          username: profile.username,
          mfa_enabled: profile.mfa_enabled,
        },
        { withCredentials: true }   // ⭐ REQUIRED
      );

      toast.success("Profile updated.");
    } catch (err) {
      console.error("Failed to update profile:", err);
      toast.error("Failed to update profile.");
    }
  };

  // ------------------------------------------------------------
  // MFA handlers (FIXED: send cookies)
  // ------------------------------------------------------------
  const handleMfaStart = async () => {
    try {
      const res = await apiClient.post(
        "/api/auth/mfa/enable",
        {},
        { withCredentials: true }   // ⭐ REQUIRED
      );

      setMfaQr(res.data.qr);
      setMfaSecret(res.data.secret);
      toast.success("MFA setup started. Scan the QR code.");
    } catch (err) {
      console.error("Failed to enable MFA:", err);
      toast.error("Failed to update MFA settings.");
    }
  };

  const handleMfaVerify = async (code) => {
    try {
      await apiClient.post(
        "/api/auth/mfa/verify",
        { code },
        { withCredentials: true }   // ⭐ REQUIRED
      );

      setProfile((prev) => ({ ...prev, mfa_enabled: true }));
      setMfaQr(null);
      setMfaSecret(null);

      toast.success("MFA enabled successfully.");
    } catch (err) {
      console.error("Failed to verify MFA:", err);
      toast.error("Failed to update MFA settings.");
    }
  };

  const handleMfaDisable = async () => {
    try {
      await apiClient.post(
        "/api/auth/mfa/disable",
        {},
        { withCredentials: true }   // ⭐ REQUIRED
      );

      setProfile((prev) => ({ ...prev, mfa_enabled: false }));
      toast.success("MFA disabled.");
    } catch (err) {
      console.error("Failed to disable MFA:", err);
      toast.error("Failed to update MFA settings.");
    }
  };

  // ------------------------------------------------------------
  // Loading skeleton
  // ------------------------------------------------------------
  if (loading) {
    return (
      <div className="profile-page-container">
        <div className="profile-section">
          <div className="skeleton skeleton-avatar"></div>
          <div className="skeleton skeleton-line" style={{ width: "60%" }}></div>
          <div className="skeleton skeleton-line" style={{ width: "40%" }}></div>
        </div>

        <div className="profile-section">
          <div className="skeleton skeleton-line" style={{ width: "50%" }}></div>
          <div className="skeleton skeleton-line"></div>
          <div className="skeleton skeleton-line"></div>
          <div className="skeleton skeleton-line" style={{ width: "80%" }}></div>
        </div>

        <div className="profile-section">
          <div className="skeleton skeleton-line" style={{ width: "50%" }}></div>
          <div className="skeleton skeleton-line"></div>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="profile-page-container">
        <div className="profile-error">Unable to load profile.</div>
      </div>
    );
  }

  // ------------------------------------------------------------
  // Tabs
  // ------------------------------------------------------------
  const tabs = {
    Avatar: (
      <AvatarUploader
        avatarUrl={profile.avatar_url}
        onUploaded={(newUrl) =>
          setProfile((prev) => ({ ...prev, avatar_url: newUrl }))
        }
      />
    ),

    Account: (
      <div className="profile-form">
        <label className="profile-label">Email</label>
        <input
          className="profile-input"
          type="email"
          value={profile.email}
          onChange={(e) =>
            setProfile({ ...profile, email: e.target.value })
          }
        />

        <label className="profile-label">Username</label>
        <input
          className="profile-input"
          type="text"
          value={profile.username}
          onChange={(e) =>
            setProfile({ ...profile, username: e.target.value })
          }
        />

        <label className="profile-label">Role</label>
        <input
          className="profile-input"
          type="text"
          value={profile.role}
          disabled
        />

        <button className="profile-button" onClick={handleSave}>
          Save Changes
        </button>
      </div>
    ),

    MFA: (
      <MFAToggle
        enabled={profile.mfa_enabled}
        qr={mfaQr}
        secret={mfaSecret}
        onStart={handleMfaStart}
        onVerify={handleMfaVerify}
        onDisable={handleMfaDisable}
      />
    ),

    Security: <ChangePasswordForm />,
  };

  return (
    <div className="profile-page-container">
      <h1 className="profile-title">Your Profile</h1>
      <ProfileTabs tabs={tabs} />
    </div>
  );
}
