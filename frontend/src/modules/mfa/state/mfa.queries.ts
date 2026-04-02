/**
 * React Query hooks for MFA.
 * These wrap the service layer and sync with Jotai state atoms.
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useSetAtom } from "jotai";

import {
  fetchMfaStatus,
  startEnrollment,
  verifyEnrollment,
  disableMfaFlow,
} from "../services/mfa.service";

import {
  mfaStatusAtom,
  mfaEnrollmentAtom,
  mfaEnrollingAtom,
  mfaDisablingAtom,
} from "./mfa.state";

// -----------------------------
// Query: MFA Status
// -----------------------------
export function useMfaStatus() {
  const setStatus = useSetAtom(mfaStatusAtom);

  return useQuery({
    queryKey: ["mfa-status"],
    queryFn: async () => {
      const status = await fetchMfaStatus();
      setStatus(status);
      return status;
    },
    staleTime: 1000 * 60, // 1 minute
  });
}

// -----------------------------
// Mutation: Begin Enrollment
// -----------------------------
export function useBeginEnrollment() {
  const setEnrollment = useSetAtom(mfaEnrollmentAtom);
  const setEnrolling = useSetAtom(mfaEnrollingAtom);

  return useMutation({
    mutationFn: async () => {
      setEnrolling(true);
      const data = await startEnrollment();
      setEnrollment(data);
      return data;
    },
    onError: () => {
      setEnrolling(false);
    },
  });
}

// -----------------------------
// Mutation: Verify Enrollment
// -----------------------------
export function useVerifyEnrollment() {
  const setEnrollment = useSetAtom(mfaEnrollmentAtom);
  const setEnrolling = useSetAtom(mfaEnrollingAtom);
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (code: string) => {
      const result = await verifyEnrollment(code);
      return result;
    },
    onSuccess: () => {
      // Clear enrollment data
      setEnrollment(null);
      setEnrolling(false);

      // Refresh MFA status
      queryClient.invalidateQueries({ queryKey: ["mfa-status"] });
    },
  });
}

// -----------------------------
// Mutation: Disable MFA
// -----------------------------
export function useDisableMfa() {
  const setDisabling = useSetAtom(mfaDisablingAtom);
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (code: string) => {
      setDisabling(true);
      const result = await disableMfaFlow(code);
      return result;
    },
    onSuccess: () => {
      setDisabling(false);

      // Refresh MFA status
      queryClient.invalidateQueries({ queryKey: ["mfa-status"] });
    },
    onError: () => {
      setDisabling(false);
    },
  });
}
