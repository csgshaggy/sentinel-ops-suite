// /src/pages/Profile/Profile.jsx
// SentinelOps — Unified Profile Page (Avatar / Account / MFA / Security)

import { useQuery } from "@tanstack/react-query";
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

export default function Profile() {
  // ------------------------------------------------------------
  // Load authenticated user profile (FULL profile, not /auth/me)
  // ------------------------------------------------------------
  const {
    data: profile,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["profile"],
    queryFn: async () => {
      const res = await apiClient.get("/profile", { withCredentials: true });
      return res.data;
    },
    retry: false,
  });

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
    Avatar: <AvatarTab profile={profile} />,
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

      <ProfileTabs tabs={tabs} />
    </div>
  );
}
