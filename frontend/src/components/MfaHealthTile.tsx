import React, { useEffect, useState } from "react";
import { Box, Text, Badge, VStack } from "@chakra-ui/react";

interface HealthStatus {
  ok: boolean;
  timestamp: string;
  message: string;
}

export default function MfaHealthTile() {
  const [status, setStatus] = useState<HealthStatus>({
    ok: true,
    timestamp: "",
    message: "Loading..."
  });

  useEffect(() => {
    async function fetchStatus() {
      try {
        const res = await fetch("/api/health/mfa");
        const data = await res.json();
        setStatus({
          ok: data.ok,
          timestamp: data.timestamp,
          message: data.message
        });
      } catch (err) {
        setStatus({
          ok: false,
          timestamp: new Date().toISOString(),
          message: "Unable to load MFA health status"
        });
      }
    }

    fetchStatus();
  }, []);

  return (
    <Box
      borderWidth="1px"
      borderRadius="lg"
      p={4}
      bg={status.ok ? "green.50" : "red.50"}
      borderColor={status.ok ? "green.300" : "red.300"}
    >
      <VStack align="start" spacing={2}>
        <Text fontSize="lg" fontWeight="bold">
          MFA Module Health
        </Text>

        <Badge
          colorScheme={status.ok ? "green" : "red"}
          fontSize="0.9em"
          px={2}
          py={1}
        >
          {status.ok ? "Healthy" : "Unhealthy"}
        </Badge>

        <Text fontSize="sm" color="gray.700">
          {status.message}
        </Text>

        <Text fontSize="xs" color="gray.500">
          Last checked: {status.timestamp}
        </Text>
      </VStack>
    </Box>
  );
}
