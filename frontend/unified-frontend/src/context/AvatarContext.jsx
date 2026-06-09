// src/context/AvatarContext.jsx
import { createContext, useContext, useState, useCallback } from "react";

const AvatarContext = createContext(null);

export function AvatarProvider({ children }) {
  const [avatarUrl, setAvatarUrl] = useState(null);
  const [avatarVersion, setAvatarVersion] = useState(Date.now());

  const updateAvatar = useCallback((baseUrl, version) => {
    const v = version || Date.now();
    setAvatarVersion(v);
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
