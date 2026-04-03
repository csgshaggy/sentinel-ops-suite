import { useEffect, useState } from "react";

// LocalStorage keys
const ROLES_KEY = "dynamic_roles";
const TILES_KEY = "dashboard_tiles";

export default function RoleManager() {
  const [roles, setRoles] = useState({});
  const [tiles, setTiles] = useState([]);
  const [newRole, setNewRole] = useState("");

  // Load roles + tiles on mount
  useEffect(() => {
    const storedRoles = JSON.parse(localStorage.getItem(ROLES_KEY) || "{}");
    const storedTiles = JSON.parse(localStorage.getItem(TILES_KEY) || "[]");

    setRoles(storedRoles);
    setTiles(storedTiles);
  }, []);

  // Save roles to localStorage
  const saveRoles = (updated) => {
    setRoles(updated);
    localStorage.setItem(ROLES_KEY, JSON.stringify(updated));
  };

  // Add a new role
  const addRole = () => {
    if (!newRole.trim()) return;

    const updated = {
      ...roles,
      [newRole]: {
        canAccess: [],
      },
    };

    saveRoles(updated);
    setNewRole("");
  };

  // Delete a role
  const deleteRole = (roleName) => {
    const updated = { ...roles };
    delete updated[roleName];
    saveRoles(updated);
  };

  // Toggle permission for a role
  const togglePermission = (roleName, tilePath) => {
    const updated = { ...roles };
    const perms = updated[roleName].canAccess;

    if (perms.includes(tilePath)) {
      updated[roleName].canAccess = perms.filter((p) => p !== tilePath);
    } else {
      updated[roleName].canAccess = [...perms, tilePath];
    }

    saveRoles(updated);
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Role Manager</h1>

      {/* Add Role */}
      <div className="flex gap-4 mb-8">
        <input
          className="border p-2 rounded flex-1"
          placeholder="New role name"
          value={newRole}
          onChange={(e) => setNewRole(e.target.value)}
        />
        <button
          onClick={addRole}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Add Role
        </button>
      </div>

      {/* Role List */}
      <div className="space-y-6">
        {Object.keys(roles).length === 0 && (
          <p className="text-gray-600">No roles defined yet.</p>
        )}

        {Object.entries(roles).map(([roleName, roleData]) => (
          <div
            key={roleName}
            className="border rounded p-4 bg-white shadow-sm"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">{roleName}</h2>

              <button
                onClick={() => deleteRole(roleName)}
                className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
              >
                Delete
              </button>
            </div>

            <h3 className="font-semibold mb-2">Permissions</h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {tiles.map((tile) => (
                <label
                  key={tile.path}
                  className="flex items-center gap-2 border p-2 rounded"
                >
                  <input
                    type="checkbox"
                    checked={roleData.canAccess.includes(tile.path)}
                    onChange={() => togglePermission(roleName, tile.path)}
                  />
                  {tile.name}
                </label>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
