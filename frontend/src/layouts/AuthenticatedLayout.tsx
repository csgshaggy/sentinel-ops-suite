import { Outlet } from "react-router-dom";
import { Box } from "@chakra-ui/react";
import { useMfaStatus } from "../modules/mfa/state/mfa.queries";
import { MfaWarningBanner } from "../modules/mfa/components/MfaWarningBanner";

export function AuthenticatedLayout() {
  const { data, isLoading, error } = useMfaStatus();

  return (
    <Box>
      {/* MFA warning banner (only shows when disabled) */}
      <MfaWarningBanner
        loading={isLoading}
        error={error}
        enabled={data?.enabled}
      />

      {/* Main app content */}
      <Outlet />
    </Box>
  );
}
