import { fetchMfaStatus } from "../modules/mfa/services/mfa.service";

export const mfaCommands = [
  {
    id: "mfa.openSettings",
    title: "Open MFA Settings",
    run: () => navigate("/settings/security/mfa"),
  },
  {
    id: "mfa.beginEnrollment",
    title: "Begin MFA Enrollment",
    run: () => navigate("/console/mfa/enroll"),
  },
  {
    id: "mfa.status",
    title: "Show MFA Status",
    async run() {
      const status = await fetchMfaStatus();
      alert(
        status.enabled
          ? "MFA is enabled for this account"
          : "MFA is disabled — enable it in Settings → Security → MFA"
      );
    },
  },
];
