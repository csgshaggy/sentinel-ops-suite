import { useRef, useState } from "react";
import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import apiClient from "../../api/apiClient";

import "./Profile.css";

import ProfileSummaryCard from "./components/ProfileSummaryCard";
import ProfileBreadcrumbs from "./components/ProfileBreadcrumbs";
import MFAStatusBadge from "./components/MFAStatusBadge";
import ProfileTabs from "./components/ProfileTabs";

import OverviewTab from "./components/tabs/OverviewTab";
import AccountTab from "./components/tabs/AccountTab";
import PersonalInfoTab from "./components/tabs/PersonalInfoTab";
import PreferencesTab from "./components/tabs/PreferencesTab";
import DevicesTab from "./components/tabs/DevicesTab";
import SecurityTab from "./components/tabs/SecurityTab";
import MFATab from "./components/tabs/MFATab";
import SessionsTab from "./components/tabs/SessionsTab";
import ApiKeysTab from "./components/tabs/ApiKeysTab";
import LoginHistoryTab from "./components/tabs/LoginHistoryTab";
import AvatarTab from "./components/tabs/AvatarTab";

/* ------------------------------------------------------------
   Helpers
------------------------------------------------------------ */

function getApiBaseUrl() {
  const configuredBase = apiClient?.defaults?.baseURL || "";
  return configuredBase.replace(/\/+$/, "");
}

function resolveAvatarUrl(url) {
  if (!url) return "/default-avatar.png";

  if (/^https?:\/\//i.test(url)) {
    return url;
  }

  const normalizedPath = url.startsWith("/") ? url : `/${url}`;
  const base = getApiBaseUrl();

  return base ? `${base}${normalizedPath}` : normalizedPath;
}

function addCacheBust(url, version) {
  if (!url) return url;
  const separator = url.includes("?") ? "&" : "?";
  const safeVersion = version || Date.now();
  return `${url}${separator}v=${encodeURIComponent(safeVersion)}`;
}

function normalizeProfile(profile) {
  if (!profile) return profile;

  const rawAvatar =
    profile.avatar_thumb_url ||
    profile.avatar_url ||
    profile.avatarThumbUrl ||
    null;

  const normalizedAvatar = addCacheBust(
    resolveAvatarUrl(rawAvatar),
    profile.avatar_version
  );

  return {
    ...profile,
    avatar_url: normalizedAvatar,
    avatar_thumb_url: normalizedAvatar,
  };
}

export default function Profile() {
  const queryClient = useQueryClient();
  const fileInputRef = useRef(null);

  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadError, setUploadError] = useState("");

  /* ------------------------------------------------------------
     Load authenticated user profile
     CORRECT ENDPOINT: /users/me
  ------------------------------------------------------------ */
  const {
    data: profile,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["profile"],
    queryFn: async () => {
      const res = await apiClient.get("/users/me", {
        withCredentials: true,
      });
      return normalizeProfile(res.data);
    },
    retry: false,
  });

  /* ------------------------------------------------------------
     Avatar upload mutation (Corrected)
     - Backend expects field name: "file"
     - Uses multipart/form-data
     - Cache-busts avatar URL
     - Updates React Query cache
  ------------------------------------------------------------ */
  const avatarUploadMutation = useMutation({
    mutationFn: async (file) => {
      const formData = new FormData();

      // Correct field name for FastAPI UploadFile
      formData.append("file", file);

      setUploadError("");
      setUploadProgress(0);

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

    onSuccess: async (data) => {
      const newAvatarUrl = addCacheBust(
        resolveAvatarUrl(data?.avatar_url),
        data?.avatar_version
      );

      // Optimistic update
      queryClient.setQueryData(["profile"], (oldProfile) => {
        if (!oldProfile) return oldProfile;

        return normalizeProfile({
          ...oldProfile,
          avatar_url: newAvatarUrl,
          avatar_thumb_url: newAvatarUrl,
          avatar_version: data?.avatar_version,
        });
      });

      // Re-fetch authoritative profile
      await queryClient.invalidateQueries({
        queryKey: ["profile"],
      });
    },

    onError: (err) => {
      setUploadError(
        err?.response?.data?.detail ||
          err?.message ||
          "Avatar upload failed."
      );
    },

    onSettled: () => {
      setTimeout(() => {
        setUploadProgress(0);
      }, 400);
    },
  });

  const handleChooseAvatar = () => {
    fileInputRef.current?.click();
  };

  const handleAvatarSelected = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setUploadError("Please choose a valid image file.");
      event.target.value = "";
      return;
    }

    avatarUploadMutation.mutate(file);

    event.target.value = "";
  };

  if (isLoading) {
    return (
      <div className="profile-page fade-in">
        <div className="profile-loading">Loading profile…</div>
      </div>
    );
  }

  if (isError || !profile) {
    return (
      <div className="profile-page fade-in">
        <div className="profile-error">
          Unable to load profile.
          <br />
          {error?.response?.data?.detail || "Unknown error"}
        </div>
      </div>
    );
  }

  const tabs = {
    Overview: <OverviewTab profile={profile} />,
    Account: <AccountTab profile={profile} />,
    "Personal Info": <PersonalInfoTab profile={profile} />,
    Preferences: <PreferencesTab profile={profile} />,
    Devices: <DevicesTab profile={profile} />,
    Avatar: (
      <AvatarTab
        profile={profile}
        onChooseAvatar={handleChooseAvatar}
        onAvatarSelected={handleAvatarSelected}
        isUploading={avatarUploadMutation.isPending}
        uploadProgress={uploadProgress}
        uploadError={uploadError}
      />
    ),
    Security: <SecurityTab profile={profile} />,
    "Multi‑Factor Auth": <MFATab profile={profile} />,
    Sessions: <SessionsTab profile={profile} />,
    "API Keys": <ApiKeysTab profile={profile} />,
    "Login History": <LoginHistoryTab profile={profile} />,
  };

  return (
    <div className="profile-page fade-in">
      <ProfileBreadcrumbs />

      <ProfileSummaryCard
        fullName={profile.full_name}
        email={profile.email}
        role={profile.role}
        avatarUrl={profile.avatar_thumb_url || profile.avatar_url}
      />

      <div className="profile-status-row">
        <MFAStatusBadge enabled={profile.mfa_enabled} />
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        hidden
        onChange={handleAvatarSelected}
      />

      <ProfileTabs tabs={tabs} />
    </div>
  );
}
