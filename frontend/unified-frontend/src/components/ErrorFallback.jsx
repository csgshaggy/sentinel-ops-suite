// /src/components/ErrorFallback.jsx

export default function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h1>Something went wrong</h1>
      <p style={{ color: "#ff6b6b" }}>{error?.message}</p>

      <button
        onClick={resetErrorBoundary}
        style={{
          marginTop: "1rem",
          padding: "0.75rem 1.5rem",
          background: "#0ff",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        Retry
      </button>
    </div>
  );
}
