/**
 * MFA store: a typed, centralized interface for reading/writing
 * MFA-related state atoms. This keeps components clean and prevents
 * direct atom imports all over the codebase.
 */

import { useAtom, useSetAtom } from "jotai";

import {
  mfaStatusAtom,
  mfaEnrollmentAtom,
  mfaEnrollingAtom,
  mfaDisablingAtom,
} from "./mfa.state";

export function useMfaStore() {
  const [status, setStatus] = useAtom(mfaStatusAtom);
  const [enrollment, setEnrollment] = useAtom(mfaEnrollmentAtom);
  const [isEnrolling, setIsEnrolling] = useAtom(mfaEnrollingAtom);
  const [isDisabling, setIsDisabling] = useAtom(mfaDisablingAtom);

  return {
    // state
    status,
    enrollment,
    isEnrolling,
    isDisabling,

    // setters
    setStatus,
    setEnrollment,
    setIsEnrolling,
    setIsDisabling,
  };
}

// Optional: write-only helpers for mutations
export const useMfaActions = () => {
  const setStatus = useSetAtom(mfaStatusAtom);
  const setEnrollment = useSetAtom(mfaEnrollmentAtom);
  const setIsEnrolling = useSetAtom(mfaEnrollingAtom);
  const setIsDisabling = useSetAtom(mfaDisablingAtom);

  return {
    setStatus,
    setEnrollment,
    setIsEnrolling,
    setIsDisabling,
  };
};
