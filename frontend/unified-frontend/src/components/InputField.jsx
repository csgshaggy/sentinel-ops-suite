import "./InputField.css";

export default function InputField({
  label,
  type = "text",
  value,
  onChange,
  className = "",
  ...props
}) {
  return (
    <div className={`input-field ${className}`}>
      {label && <label>{label}</label>}
      <input type={type} value={value} onChange={onChange} {...props} />
    </div>
  );
}
