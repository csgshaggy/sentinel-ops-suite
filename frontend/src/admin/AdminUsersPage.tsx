import { useEffect, useState } from "react";
import {
  fetchUsers,
  toggleUserActive,
  resetUserPassword,
} from "../../api/adminUsers";
import UserRow from "../../components/admin/UserRow";

export default function AdminUsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      const data = await fetchUsers();
      setUsers(data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleToggle(id, current) {
    await toggleUserActive(id, !current);
    load();
  }

  async function handleReset(id) {
    const result = await resetUserPassword(id);
    alert(`Temporary password: ${result.temporary_password}`);
  }

  if (loading) return <div>Loading users…</div>;

  return (
    <div>
      <h2>User Management</h2>

      <table className="admin-table">
        <thead>
          <tr>
            <th>Email</th>
            <th>Role</th>
            <th>Last Login</th>
            <th>Session</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {users.map((u) => (
            <UserRow
              key={u.id}
              user={u}
              onToggle={() => handleToggle(u.id, u.is_active)}
              onReset={() => handleReset(u.id)}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
