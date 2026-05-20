import "../styles/theme.css";
import "../styles/global.css";
import "./Panel.css";

export default function Panel({ title, children }) {
  return (
    <div className="panel">
      {title && <div className="panel-header">{title}</div>}
      <div className="panel-content">{children}</div>
    </div>
  );
}
