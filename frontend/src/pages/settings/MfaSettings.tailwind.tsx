import { useEffect, useState } from "react";
import { Box, Button, Heading, Text } from "@chakra-ui/react";

export default function MfaSettingsChakra() {
  const [verify, setVerify] = useState<any>(null);

  useEffect(() => {
    import("../../features/mfa-query/useVerifyMfa").then((mod) => {
      setVerify(() => mod.useVerifyMfa());
    });
  }, []);

  if (!verify) return <Text>Loading MFA module…</Text>;

  return (
    <Box p={6}>
      <Heading size="lg">MFA Settings (Chakra)</Heading>
      <Text mt={4}>Manage your multi‑factor authentication settings.</Text>

      <Button mt={6} colorScheme="blue" onClick={() => verify.mutate()}>
        Verify MFA
      </Button>
    </Box>
  );
}
