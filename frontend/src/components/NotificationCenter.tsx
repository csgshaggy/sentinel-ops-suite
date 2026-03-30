import React, { useState } from "react";

export interface Notification {
  id: string;
  message: string;
  type?: "info" | "success" | "warning" | "error";
}

const NotificationCenter: React.FC = () => {
  const [notifications] = useState<Notification[]>([]);

  if (!notifications.length) return null;

  return (
    <div className="notification-center">
      {notifications.map((n) => (
        <div key={n.id} className={`notification ${n.type ?? "info"}`}>
          {n.message}
        </div>
      ))}
    </div>
  );
};

export default NotificationCenter;
