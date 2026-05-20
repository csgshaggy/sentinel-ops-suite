import { Box, Text, Badge, Spinner } from "@chakra-ui/react";
import { useMfaStatus } from "../state/mfa.queries";
import { Link } from "react-router-dom";

export function MfaStatusTile() {
  const { data, isLoading, error } = useMfaStatus();

  return (
    <Link to="/settings/security/mfa">
      <Box
        p={5}
        borderWidth="1px"
        borderRadius="lg"
        _hover={{ bg: "gray.50" }}
        transition="0.2s"
      >
        <Text fontSize="lg" fontWeight="bold">
          Multi‑Factor Authentication
        </Text>

        {isLoading && <Spinner mt={3} />}

        {error && (
          <Badge mt={3} colorScheme="red">
            Error
          </Badge>
        )}

        {data && (
          <Badge
            mt={3}
            colorScheme={data.enabled ? "green" : "yellow"}
          >
            {data.enabled ? "Enabled" : "Disabled"}
          </Badge>
        )}
      </Box>
    </Link>
  );
}
