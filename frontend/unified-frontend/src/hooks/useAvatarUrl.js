// /src/hooks/useAvatarUrl.js
// SentinelOps — Deterministic Avatar URL Resolver
// - Uses backend avatar_url when present
// - Falls back to static default avatar
// - Always returns an absolute URL for the browser

import { useMemo } from "react";

export default function useAvatarUrl(user) {
  return useMemo(() => {
    if (!user) return null;

    // Backend returns:
    //   avatar_url: "/static/avatars/<id>_avatar.png?t=123456"
    //   OR null
    //
    // Default avatar is:
    //   /static/avatars/default-avatar.png

    const url = user.avatar_url;

    // If backend provided a valid avatar URL → use it
    if (url && typeof url === "string") {
      if (url.startsWith("/")) {
        return `${window.location.origin}${url}`;
      }
      return url;
    }

    // Fallback to default avatar (correct path)
    return `${window.location.origin}/static/avatars/default-avatar.png`;
  }, [user?.avatar_url]);
}
