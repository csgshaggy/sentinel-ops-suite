import { CheckCircleIcon, WarningIcon } from "@chakra-ui/icons";
import {
  Badge,
  Box,
  Heading,
  HStack,
  Icon,
  Spinner,
  Text,
  VStack,
} from "@chakra-ui/react";
import React from "react";

import { useMfaStatus } from "../../features/mfa-query/useMfaStatus";

export default function MfaStatusTile() {
  const status = useMfaStatus();

  return (
    <Box
      p={5}
      borderRadius="md"
      bg="gray.800"
      border="1px solid"
      borderColor="gray.700"
      shadow="md"
      minH="150px"
    >
      <Heading size="md" mb={3}>
        MFA Status
      </Heading>

      {/* Loading State */}
      {status.isLoading && (
        <HStack>
          <Spinner size="sm" />
          <Text>Checking MFA status…</Text>
        </HStack>
      )}

      {/* Error State */}
      {status.isError && (
        <HStack color="red.300">
          <Icon as={WarningIcon} />
          <Text>Error loading MFA status</Text>
        </HStack>
      )}

      {/* Enabled State */}
      {status.data?.enabled && (
        <VStack align="start" spacing={2}>
          <HStack>
            <Icon as={CheckCircleIcon} color="green.300" />
            <Text fontWeight="bold" color="green.300">
              Enabled
            </Text>
          </HStack>

          <Badge colorScheme="green" variant="subtle">
            Secure
          </Badge>

          <Text fontSize="sm" color="gray.400">
            MFA is active on this account.
          </Text>
        </VStack>
      )}

      {/* Disabled State */}
      {status.data && !status.data.enabled && (
        <VStack align="start" spacing={2}>
          <HStack>
            <Icon as={WarningIcon} color="yellow.300" />
            <Text fontWeight="bold" color="yellow.300">
              Disabled
            </Text>
          </HStack>

          <Badge colorScheme="yellow" variant="subtle">
            Action Required
          </Badge>

          <Text fontSize="sm" color="gray.400">
            MFA is not enabled. Consider enabling it for better security.
          </Text>
        </VStack>
      )}
    </Box>
  );
}
