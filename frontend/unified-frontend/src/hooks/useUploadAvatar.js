// src/hooks/useAvatarUrl.js
// SentinelOps — Global Avatar Cache-Busting Hook (Final Version)

import { useEffect, useState } from "react";

export default function useAvatarUrl(profile) {
  const [url, setUrl] = useState(null);

  useEffect(() => {
    if (!profile) {
      setUrl(null);
      return;
    }

    const base =
      profile.avatar_thumb_url ||
      profile.avatar_url ||
      "/static/default-avatar.png";

    const version = profile.avatar_version || Date.now();

    // ⭐ Always append version to force browser refresh
    setUrl(`${base}?v=${version}`);
  }, [
    profile?.avatar_url,
    profile?.avatar_thumb_url,
    profile?.avatar_version,
  ]);

  return url;
}
