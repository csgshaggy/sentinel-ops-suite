// /src/hooks/useAvatar.js
// SentinelOps — Unified Avatar Resolver
// - Wraps useAvatarUrl()
// - Adds optional cache-busting
// - Provides stable return shape for UI components

import { useMemo } from "react";
import useAvatarUrl from "./useAvatarUrl";

export default function useAvatar(user, { bustCache = false } = {}) {
  const baseUrl = useAvatarUrl(user);

  return useMemo(() => {
    if (!baseUrl) {
      return {
        url: null,
        cacheBustedUrl: null,
      };
    }

    // Optional cache-busting for components that need it
    const cacheBustedUrl = bustCache
      ? `${baseUrl}?t=${Date.now()}`
      : baseUrl;

    return {
      url: baseUrl,
      cacheBustedUrl,
    };
  }, [baseUrl, bustCache]);
}
