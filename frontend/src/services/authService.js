// /home/ubuntu/sentinel-ops-suite/frontend/src/services/authService.js

import api from "../config/api";

export const login = async (username, password) => {
  const response = await api.post("/auth/login", {
    username,
    password,
  });
  return response.data;
};

export const logout = async () => {
  const response = await api.post("/auth/logout");
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get("/users/me");
  return response.data;
};
