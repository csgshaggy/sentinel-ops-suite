// =====================================================================
// SSRF Command Console — NotificationContext
// Global toast system • Auto-dismiss • Theme-compatible
// =====================================================================

import { createContext, ReactNode, useCallback,useContext, useState } from "react";

export type NotificationType = "info" | "success" | "error";

export type Notification = {
  id: string;
  type: NotificationType;
  message: string;
};

type NotificationContextType = {
  notifications: Notification[];
  push: (n: Omit<Notification, "id">) => void;
  remove: (id: string) => void;
};

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export function NotificationProvider({ children }: { children: ReactNode }) {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const remove = useCallback((id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  const push = useCallback(
    (n: Omit<Notification, "id">) => {
      const id = crypto.randomUUID();
      const full = { ...n, id };

      setNotifications((prev) => [...prev, full]);

      // Auto-dismiss after 4 seconds
      setTimeout(() => remove(id), 4000);
    },
    [remove]
  );

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        push,
        remove,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
}

export function useNotifications() {
  const ctx = useContext(NotificationContext);
  if (!ctx) {
    throw new Error("useNotifications must be used within NotificationProvider");
  }
  return ctx;
}
