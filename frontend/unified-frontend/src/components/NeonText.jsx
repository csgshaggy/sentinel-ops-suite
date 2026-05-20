import "./NeonText.css";

export default function NeonText({ children, className = "" }) {
  return <span className={`neon-text ${className}`}>{children}</span>;
}
