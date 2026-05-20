import {
  MfaStatus,
  MfaEnrollmentResponse,
  MfaVerifyResponse,
  MfaDisableResponse,
  MfaError,
} from "./mfa.types";

import {
  getMfaStatus,
  beginMfaEnrollment,
  verifyMfaEnrollment,
  disableMfa,
} from "./mfa.api";

/**
 * Service layer for MFA orchestration.
 * This wraps API calls, normalizes responses, and provides
 * deterministic shapes for React Query hooks and UI components.
 */

export async function fetchMfaStatus(): Promise<MfaStatus> {
  return getMfaStatus();
}

export async function startEnrollment(): Promise<MfaEnrollmentResponse> {
  return beginMfaEnrollment();
}

export async function verifyEnrollment(code: string): Promise<MfaVerifyResponse> {
  if (!code || code.length !== 6) {
    throw <MfaError>{
      message: "Invalid code format",
      code: "INVALID_CODE",
    };
  }
  return verifyMfaEnrollment(code);
}

export async function disableMfaFlow(code: string): Promise<MfaDisableResponse> {
  if (!code || code.length !== 6) {
    throw <MfaError>{
      message: "Invalid code format",
      code: "INVALID_CODE",
    };
  }
  return disableMfa(code);
}
