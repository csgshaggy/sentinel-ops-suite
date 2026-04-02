import { Navigate } from "react-router-dom";
import { useMfaStatus } from "../../modules/mfa/state/mfa.queries";

export function RequireMfa({ children }: { children: JSX.Element }) {
  const { data, isLoading } = useMfaStatus();

  if (isLoading) return null;

  if (!data?.enabled) {
    return <Navigate to="/console/mfa" replace />;
  }

  return children;
}
