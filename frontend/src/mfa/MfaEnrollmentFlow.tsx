import {
  Box,
  Heading,
  Text,
  Image,
  Input,
  Button,
  Spinner,
} from "@chakra-ui/react";

import {
  useBeginEnrollment,
  useVerifyEnrollment,
  useMfaStatus,
} from "../../modules/mfa/state/mfa.queries";

export function MfaEnrollmentFlow() {
  const { data: status } = useMfaStatus();
  const begin = useBeginEnrollment();
  const verify = useVerifyEnrollment();

  const [code, setCode] = useState("");

  // If MFA already enabled, redirect or show message
  if (status?.enabled) {
    return (
      <Box>
        <Heading size="md">MFA Already Enabled</Heading>
        <Text mt={2}>Your account is already protected.</Text>
      </Box>
    );
  }

  // Begin enrollment automatically
  useEffect(() => {
    if (!begin.data && !begin.isLoading) {
      begin.mutate();
    }
  }, []);

  if (begin.isLoading || !begin.data) {
    return <Spinner />;
  }

  return (
    <Box>
      <Heading size="lg">Set Up MFA</Heading>

      <Text mt={4}>
        Scan this QR code with your authenticator app.
      </Text>

      <Image
        src={begin.data.qrCodeDataUrl}
        alt="MFA QR Code"
        mt={4}
        borderRadius="md"
      />

      <Text mt={6}>Enter the 6‑digit code from your app:</Text>

      <Input
        mt={2}
        value={code}
        onChange={(e) => setCode(e.target.value)}
        maxLength={6}
        width="200px"
      />

      <Button
        mt={4}
        colorScheme="green"
        onClick={() => verify.mutate(code)}
        isLoading={verify.isLoading}
      >
        Verify & Enable MFA
      </Button>

      {verify.isSuccess && (
        <Text mt={4} color="green.500">
          MFA enabled successfully!
        </Text>
      )}
    </Box>
  );
}
