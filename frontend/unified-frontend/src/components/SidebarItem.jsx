import { Link } from "react-router-dom";

export default function SidebarItem({
  icon,
  label,
  to,
  active,
}) {
  return (
    <Link
      to={to}
      className={`sidebar-item ${active ? "active" : ""}`}
    >
      {icon}
      <span>{label}</span>
    </Link>
  );
}
