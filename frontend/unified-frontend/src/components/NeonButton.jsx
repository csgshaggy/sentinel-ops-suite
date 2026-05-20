import "./NeonButton.css";

export default function NeonButton({
  children,
  onClick,
  type = "button",
  className = "",
  ...props
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`neon-button ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
