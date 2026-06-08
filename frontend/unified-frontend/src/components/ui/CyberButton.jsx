export default function CyberButton({
  children,
  variant = "primary",
  className = "",
  ...props
}) {
  const base = "btn px-4 py-2";

  const variants = {
    primary: "btn-primary",
    secondary: "btn-secondary",
    danger: "btn-danger",
  };

  return (
    <button
      className={`${base} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
