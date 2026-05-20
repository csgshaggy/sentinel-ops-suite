export default function UserRow({ user, onToggle, onReset }) {
  return (
    <tr>
      <td>{user.email}</td>
      <td>{user.role}</td>
      <td>{user.last_login || "—"}</td>
      <td>{user.session_active ? "Active" : "None"}</td>
      <td>{user.is_active ? "Enabled" : "Disabled"}</td>

      <td>
        <button onClick={onReset}>Reset Password</button>

        <button
          style={{
            marginLeft: "0.5rem",
            background: user.is_active ? "var(--danger)" : "var(--accent)",
          }}
          onClick={onToggle}
        >
          {user.is_active ? "Disable" : "Enable"}
        </button>
      </td>
    </tr>
  );
}
