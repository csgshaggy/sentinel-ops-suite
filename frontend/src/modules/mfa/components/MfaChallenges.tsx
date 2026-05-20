import React, { useState } from "react";
import {
  Box,
  Heading,
  Text,
  VStack,
  Alert,
  AlertIcon,
  Spinner,
} from "@chakra-ui/react";
import TotpInput from "./TotpInput";

interface MfaChallengeProps {
  onSubmit: (code: string) => Promise<void>;
  loading?: boolean;
}

const MfaChallenge: React.FC<MfaChallengeProps> = ({ onSubmit, loading = false }) => {
  const [status, setStatus] = useState<"idle" | "verifying" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const handleComplete = async (code: string) => {
    try {
      setStatus("verifying");
      setErrorMessage("");

      await onSubmit(code);

      // If successful, the parent flow will redirect or update state.
    } catch (err: any) {
      setStatus("error");
      setErrorMessage(err?.message || "Invalid code. Try again.");
    }
  };

  return (
    <Box>
      <Heading size="md" mb={4}>
        Multi‑Factor Authentication
      </Heading>

      <VStack spacing={4} align="stretch">
        <Text>
          Enter the 6‑digit authentication code from your authenticator app to continue.
        </Text>

        <TotpInput onComplete={handleComplete} />

        {(loading || status === "verifying") && (
          <Alert status="info">
            <AlertIcon />
            <Spinner size="sm" mr={2} /> Verifying code…
          </Alert>
        )}

        {status === "error" && (
          <Alert status="error">
            <AlertIcon />
            {errorMessage}
          </Alert>
        )}
      </VStack>
    </Box>
  );
};

export default MfaChallenge;
