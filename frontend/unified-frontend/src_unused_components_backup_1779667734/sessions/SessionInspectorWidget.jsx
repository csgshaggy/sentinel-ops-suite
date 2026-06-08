// /src/components/widgets/sessions/SessionInspectorWidget.jsx

export default function SessionInspectorWidget() {
  return (
    <div>
      <strong>Session Inspector:</strong>
      <p>No session selected.</p>

      <div style={{ marginTop: "12px" }}>
        <p><strong>Session ID:</strong> —</p>
        <p><strong>User ID:</strong> —</p>
        <p><strong>IP Address:</strong> —</p>
        <p><strong>User Agent:</strong> —</p>
        <p><strong>Issued At:</strong> —</p>
        <p><strong>Expires At:</strong> —</p>
        <p><strong>Last Activity:</strong> —</p>
        <p><strong>Device:</strong> —</p>
        <p><strong>Status:</strong> —</p>
      </div>
    </div>
  );
}
