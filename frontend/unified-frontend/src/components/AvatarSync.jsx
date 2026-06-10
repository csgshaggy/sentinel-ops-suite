import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";

// ✔ Correct API import (profile.js exists)
import { fetchProfile } from "../api/profile.js";

// ✔ Correct AvatarContext import (AvatarContext.jsx exists)
import { useAvatarContext } from "../context/AvatarContext.jsx";

export default function AvatarSync() {
  const { data: profile } = useQuery(["profile"], fetchProfile);
  const { updateAvatar } = useAvatarContext();

  useEffect(() => {
    if (!profile) return;

    const base =
      profile.avatar_thumb_url ||
      profile.avatar_url ||
      "/static/default-avatar.png";

    updateAvatar(base, profile.avatar_version);
  }, [profile, updateAvatar]);

  return null;
}
