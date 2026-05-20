// /src/context/UserMenuContext.jsx

import { createContext, useContext } from "react";

const UserMenuContext = createContext({
  isOpen: false,
  toggle: () => {},
  close: () => {},
});

export function UserMenuProvider({ children }) {
  // Placeholder provider — safe no‑op
  return (
    <UserMenuContext.Provider
      value={{
        isOpen: false,
        toggle: () => {},
        close: () => {},
      }}
    >
      {children}
    </UserMenuContext.Provider>
  );
}

export function useUserMenu() {
  return useContext(UserMenuContext);
}
