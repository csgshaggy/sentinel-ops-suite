// /src/components/RouteErrorBoundary.jsx

import { ErrorBoundary } from "react-error-boundary";
import ErrorFallback from "./ErrorFallback.jsx";

export default function RouteErrorBoundary({ children }) {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => {
        // Reload the route on reset
        window.location.reload();
      }}
    >
      {children}
    </ErrorBoundary>
  );
}
