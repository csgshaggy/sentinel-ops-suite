import React, { createContext, useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import SessionExpireModal from "./SessionExpireModal.jsx";

const SessionExpireContext = createContext();

export function useSessionExpire() {
  return useContext(SessionExpireContext);
}

export function SessionExpireProvider({ children }) {
  const [visible, setVisible] = useState(false);
  const navigate = useNavigate();

  const showModal = () => setVisible(true);
  const hideModal = () => setVisible(false);

  const handleLogout = () => {
    fetch("/api/auth/logout", {
      method: "POST",
      credentials: "include",
    }).finally(() => {
      // IMPORTANT:
      // Because BrowserRouter uses basename="/admin",
      // navigate("/login") becomes /admin/login automatically.
      navigate("/login", { replace: true });
    });
  };

  return (
    <SessionExpireContext.Provider value={{ showModal, hideModal }}>
      {children}
      <SessionExpireModal visible={visible} onLogout={handleLogout} />
    </SessionExpireContext.Provider>
  );
}
