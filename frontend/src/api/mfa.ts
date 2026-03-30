import axios from "./axiosInstance";

export const getMfaStatus = () => axios.get("/auth/mfa/status");

export const enrollMfa = () => axios.post("/auth/mfa/enroll");

export const verifyEnrollment = (code: string) =>
  axios.post("/auth/mfa/verify-enrollment", { code });

export const disableMfa = (code: string) => axios.post("/auth/mfa/disable", { code });

export const verifyLoginMfa = (userId: number, code: string) =>
  axios.post("/auth/login/mfa", { user_id: userId, code });
