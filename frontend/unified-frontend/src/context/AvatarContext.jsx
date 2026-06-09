const DEFAULT_AVATAR = "/static/default-avatar.png";
// src/context/AvatarContext.jsx
import { createContext, useContext, useState, useCallback } from "react";

const AvatarContext = createContext(null);

export function AvatarProvider({ children }) {
  const [avatarUrl, setAvatarUrl] = useState(null);
  const [avatarVersion, setAvatarVersion] = useState(Date.now());

  const updateAvatar = useCallback((baseUrl, version) => {
    const v = version || Date.now();
    const finalUrl = baseUrl ? `${baseUrl}?v=${v}` : DEFAULT_AVATAR;

    const img = new Image();
    img.src = finalUrl;

    const finalUrl = baseUrl ? `${baseUrl}?v=${v}` : DEFAULT_AVATAR;

    const img = new Image();
    img.src = finalUrl;

    setAvatarVersion(v);
    setAvatarUrl(finalUrl);
    setAvatarUrl(finalUrl);
    setAvatarUrl(`${baseUrl}?v=${v}`);
  }, []);

  return (
    <AvatarContext.Provider
      value={{
        avatarUrl,
        avatarVersion,
        updateAvatar,
      }}
    >
      {children}
    </AvatarContext.Provider>
  );
}

export function useAvatarContext() {
  return useContext(AvatarContext);
}
