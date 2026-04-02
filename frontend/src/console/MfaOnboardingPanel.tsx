import { Box, Heading, Text, Button, Spinner } from "@chakra-ui/react";
import { useMfaStatus } from "../../modules/mfa/state/mfa.queries";
import { Link } from "react-router-dom";

export function MfaOnboardingPanel() {
  const { data, isLoading } = useMfaStatus();

  if (isLoading) {
    return <Spinner />;
  }

  if (data?.enabled) {
    return (
      <Box>
        <Heading size="md">MFA Already Enabled</Heading>
        <Text mt={2}>
          Your account is fully protected with multi‑factor authentication.
        </Text>
      </Box>
    );
  }

  return (
    <Box>
      <Heading size="lg">Secure Your Account</Heading>
      <Text mt={3}>
        MFA adds an extra layer of protection. Let’s get you set up.
      </Text>

      <Button
        as={Link}
        to="/console/mfa/enroll"
        mt={6}
        colorScheme="blue"
      >
        Begin MFA Enrollment
      </Button>
    </Box>
  );
}
