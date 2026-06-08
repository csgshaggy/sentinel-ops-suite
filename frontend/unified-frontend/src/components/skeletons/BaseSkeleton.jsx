// /src/components/skeletons/BaseSkeleton.jsx

export default function BaseSkeleton({ height = "20px", width = "100%", style = {} }) {
  return (
    <div
      style={{
        background: "rgba(255,255,255,0.08)",
        borderRadius: "6px",
        marginBottom: "12px",
        height,
        width,
        animation: "pulse 1.4s ease-in-out infinite",
        ...style,
      }}
    />
  );
}
