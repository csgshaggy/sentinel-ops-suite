// /home/ubuntu/sentinel-ops-suite/frontend/src/api/clients.ts

import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL;

export const apiClient = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
});
