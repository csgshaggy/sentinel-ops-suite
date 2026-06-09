import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchProfile } from "../api/profileClient";
import { useAvatarContext } from "../context/AvatarContext";

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
  }, [profile]);

  return null;
}
