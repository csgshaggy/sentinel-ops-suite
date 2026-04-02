import React, { useState } from "react";
import {
  Box,
  Button,
  Heading,
  Text,
  VStack,
  Alert,
  AlertIcon,
  Spinner,
  Switch,
  HStack,
} from "@chakra-ui/react";
import MfaEnrollment from "./MfaEnrollment";
import TotpInput from "./TotpInput";

interface MfaSettingsProps {
  mfaEnabled: boolean;
  qrCodeDataUrl?: string | null;
  secret?: string | null;

  onBeginEnrollment: () => Promise<void>;
  onVerifyEnrollment: (code: string) => Promise<void>;
  onDisableMfa: (code: string) => Promise<void>;
}

const MfaSettings: React.FC<MfaSettingsProps> = ({
  mfaEnabled,
  qrCodeDataUrl,
  secret,
  onBeginEnrollment,
  onVerifyEnrollment,
  onDisableMfa,
}) => {
  const [mode, setMode] = useState<"idle" | "enrolling" | "disabling">("idle");
  const [status, setStatus] = useState<"idle" | "working" | "error" | "success">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const startEnrollment = async () => {
    try {
      setStatus("working");
      setErrorMessage("");
      await onBeginEnrollment();
      setMode("enrolling");
      setStatus("idle");
    } catch (err: any) {
      setStatus("error");
      setErrorMessage(err?.message || "Failed to start MFA enrollment.");
    }
  };

  const handleDisable = async (code: string) => {
    try {
      setStatus("working");
      setErrorMessage("");
      await onDisableMfa(code);
      setStatus("success");
      setMode("idle");
    } catch (err: any) {
      setStatus("error");
      setErrorMessage(err?.message || "Failed to disable MFA.");
    }
  };

  return (
    <Box>
      <Heading size="md" mb={4}>
        Multi‑Factor Authentication Settings
      </Heading>

      {mode === "idle" && (
        <VStack align="stretch" spacing={4}>
          <HStack justify="space-between">
            <Text fontWeight="medium">MFA Status</Text>
            <Switch isChecked={mfaEnabled} isReadOnly />
          </HStack>

          {mfaEnabled ? (
            <Box>
              <Text mb={2}>To disable MFA, enter a valid authentication code:</Text>
              <TotpInput onComplete={handleDisable} />
            </Box>
          ) : (
            <Button colorScheme="blue" onClick={startEnrollment}>
              Enable MFA
            </Button>
          )}

          {status === "working" && (
            <Alert status="info">
              <AlertIcon />
              <Spinner size="sm" mr={2} /> Processing…
            </Alert>
          )}

          {status === "error" && (
            <Alert status="error">
              <AlertIcon />
              {errorMessage}
            </Alert>
          )}

          {status === "success" && (
            <Alert status="success">
              <AlertIcon />
              MFA updated successfully.
            </Alert>
          )}
        </VStack>
      )}

      {mode === "enrolling" && (
        <MfaEnrollment
          qrCodeDataUrl={qrCodeDataUrl || null}
          secret={secret || null}
          onVerify={onVerifyEnrollment}
          onCancel={() => setMode("idle")}
        />
      )}
    </Box>
  );
};

export default MfaSettings;
