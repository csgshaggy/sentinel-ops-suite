/**
 * Lightweight client-side state container for MFA.
 * This is NOT global Redux — it's module-local state
 * used by React Query hooks and UI components.
 */

import { atom } from "jotai";
import {
  MfaStatus,
  MfaEnrollmentResponse,
} from "../services/mfa.types";

// Whether MFA is currently enabled for the user
export const mfaStatusAtom = atom<MfaStatus | null>(null);

// Enrollment data returned from backend (QR + secret)
export const mfaEnrollmentAtom = atom<MfaEnrollmentResponse | null>(null);

// Tracks whether the user is currently in an enrollment flow
export const mfaEnrollingAtom = atom<boolean>(false);

// Tracks whether the user is currently disabling MFA
export const mfaDisablingAtom = atom<boolean>(false);
