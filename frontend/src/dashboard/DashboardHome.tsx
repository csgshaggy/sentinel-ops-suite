import { Box, Grid } from "@chakra-ui/react";
import { useMfaStatus } from "../modules/mfa/state/mfa.queries";
import { MfaWarningBanner } from "../modules/mfa/components/MfaWarningBanner";

import { SystemHealthTile } from "./tiles/SystemHealthTile";
import { RepoHealthTile } from "./tiles/RepoHealthTile";
import { SessionHealthTile } from "./tiles/SessionHealthTile";
import { MfaStatusTile } from "../modules/mfa/components/MfaStatusTile";

export function DashboardHome() {
  const { data, isLoading, error } = useMfaStatus();

  return (
    <Box p={6}>
      {/* MFA reminder banner (only shows when disabled) */}
      <MfaWarningBanner
        loading={isLoading}
        error={error}
        enabled={data?.enabled}
      />

      {/* Dashboard tiles */}
      <Grid
        templateColumns="repeat(auto-fill, minmax(280px, 1fr))"
        gap={6}
        mt={4}
      >
        <SystemHealthTile />
        <RepoHealthTile />
        <SessionHealthTile />

        {/* MFA tile */}
        <MfaStatusTile />
      </Grid>
    </Box>
  );
}
