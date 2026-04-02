import {
  Alert,
  AlertIcon,
  Box,
  Button,
  Heading,
  HStack,
  Image,
  Spinner,
  Text,
  VStack,
} from "@chakra-ui/react";
import React, { useState } from "react";

import TotpInput from "../../components/mfa/TotpInput";
import { useDisableMfa } from "../../features/mfa-query/useDisableMfa";
import { useEnrollMfa } from "../../features/mfa-query/useEnrollMfa";
import { useMfaStatus } from "../../features/mfa-query/useMfaStatus";
import { useVerifyMfa } from "../../features/mfa-query/useVerifyMfa";

export default function MfaSettingsChakra() {
  const [code, setCode] = useState("");

  const status = useMfaStatus();
  const enroll = useEnrollMfa();
  const verify = useVerifyMfa();
  const disable = useDisableMfa();

  if (status.isLoading) {
    return (
      <Box p={8}>
        <HStack>
          <Spinner />
          <Text>Loading MFA status…</Text>
        </HStack>
      </Box>
    );
  }

  return (
    <Box p={8}>
      <Heading size="lg" mb={6}>
        Multi‑Factor Authentication
      </Heading>

      <VStack align="start" spacing={6}>
        {/* ---------------------- */}
        {/* MFA Disabled           */}
        {/* ---------------------- */}
        {!status.data?.enabled && !enroll.data && (
          <Button
            colorScheme="blue"
            onClick={() => enroll.mutate()}
            isLoading={enroll.isPending}
          >
            Enable MFA
          </Button>
        )}

        {/* ---------------------- */}
        {/* Enrollment Step        */}
        {/* ---------------------- */}
        {enroll.data && !status.data?.enabled && (
          <VStack align="start" spacing={4}>
            <Text>Scan this QR Code with your authenticator app:</Text>

            <Image
              src={enroll.data.qr_code}
              alt="QR Code"
              boxSize="200px"
              borderRadius="md"
            />

            <Text fontSize="sm" color="gray.400">
              Secret: {enroll.data.secret}
            </Text>

            <TotpInput value={code} onChange={setCode} />

            <Button
              colorScheme="green"
              onClick={() =>
                verify.mutate(code, { onSuccess: () => status.refetch() })
              }
              isLoading={verify.isPending}
            >
              Verify
            </Button>

            {verify.isError && (
              <Alert status="error">
                <AlertIcon />
                {(verify.error as Error).message}
              </Alert>
            )}
          </VStack>
        )}

        {/* ---------------------- */}
        {/* MFA Enabled            */}
        {/* ---------------------- */}
        {status.data?.enabled && (
          <VStack align="start" spacing={4}>
            <Alert status="success">
              <AlertIcon />
              MFA is enabled
            </Alert>

            <Button
              colorScheme="red"
              onClick={() =>
                disable.mutate(undefined, { onSuccess: () => status.refetch() })
              }
              isLoading={disable.isPending}
            >
              Disable MFA
            </Button>

            {disable.isError && (
              <Alert status="error">
                <AlertIcon />
                {(disable.error as Error).message}
              </Alert>
            )}
          </VStack>
        )}
      </VStack>
    </Box>
  );
}
