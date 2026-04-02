// Shared types for the MFA module

export interface MfaStatus {
  enabled: boolean;
}

export interface MfaEnrollmentResponse {
  qrCodeDataUrl: string;
  secret: string;
}

export interface MfaVerifyResponse {
  success: boolean;
}

export interface MfaDisableResponse {
  success: boolean;
}

export interface MfaError {
  message: string;
  code?: string;
}
