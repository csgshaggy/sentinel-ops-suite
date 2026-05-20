// dashboard-app/src/api/settingsApi.js

import api from "./api.js";   // ← correct path

export const fetchSettings = async () => {
  const response = await api.get("/settings");
  return response.data;
};

export const updateSettings = async (updates) => {
  const response = await api.put("/settings", updates);
  return response.data;
};
