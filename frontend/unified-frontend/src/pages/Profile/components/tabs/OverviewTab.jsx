// /src/pages/Profile/components/tabs/OverviewTab.jsx

export default function OverviewTab({ profile }) {
  return (
    <div className="tab-section fade-in">
      <h2 className="tab-title">Profile Overview</h2>

      <div className="tab-grid">
        <div className="tab-item">
          <label>Full Name</label>
          <div>{profile.full_name}</div>
        </div>

        <div className="tab-item">
          <label>Email</label>
          <div>{profile.email}</div>
        </div>

        <div className="tab-item">
          <label>Role</label>
          <div>{profile.role}</div>
        </div>

        <div className="tab-item">
          <label>Account Created</label>
          <div>{profile.created_at || "Unknown"}</div>
        </div>

        <div className="tab-item">
          <label>Last Login</label>
          <div>{profile.last_login || "Unknown"}</div>
        </div>

        <div className="tab-item">
          <label>Last Login IP</label>
          <div>{profile.last_login_ip || "Unknown"}</div>
        </div>
      </div>
    </div>
  );
}
