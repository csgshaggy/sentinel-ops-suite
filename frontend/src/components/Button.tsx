export function Button({ children, ...props }) {
  return (
    <button {...props} className="btn">
      {children}
    </button>
  );
}
