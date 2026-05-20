import { Alert, AlertIcon, AlertTitle, AlertDescription } from "@chakra-ui/react";
import { Link } from "react-router-dom";

interface Props {
  loading: boolean;
  error: any;
  enabled?: boolean;
}

export function MfaWarningBanner({ loading, error, enabled }: Props) {
  if (loading) return null;
  if (error) return null;
  if (enabled) return null;

  return (
    <Alert status="warning" borderRadius="md" mb={4}>
      <AlertIcon />
      <AlertTitle>MFA is not enabled</AlertTitle>
      <AlertDescription ml={2}>
        Your account is less secure.  
        <Link to="/settings/security/mfa" style={{ textDecoration: "underline" }}>
          Enable MFA now
        </Link>
      </AlertDescription>
    </Alert>
  );
}
