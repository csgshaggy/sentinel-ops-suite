// /home/ubuntu/sentinel-ops-suite/frontend/src/services/userService.js

import api from "../config/api";

export const getUserProfile = async () => {
  const response = await api.get("/users/me");
  return response.data;
};
