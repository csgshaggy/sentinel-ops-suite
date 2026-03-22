def sidebar():
    return """
    <div style="
        width: 240px;
        background: #1e1e1e;
        color: white;
        padding: 20px;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        font-family: Arial, sans-serif;
    ">
        <h2 style="margin-top: 0;">Admin Panel</h2>

        <a href="/admin" style="color: #4ea1ff; text-decoration: none;">🏠 Home</a><br><br>

        <strong>Documentation</strong><br>
        <a href="/admin/docs/dashboard" style="color: #4ea1ff; text-decoration: none;">📘 Dashboard</a><br>
        <a href="/admin/docs/search?q=test" style="color: #4ea1ff; text-decoration: none;">🔍 Search</a><br>
        <a href="/admin/docs/health" style="color: #4ea1ff; text-decoration: none;">💚 Health Score</a><br>
        <a href="/admin/docs/diff" style="color: #4ea1ff; text-decoration: none;">📊 Drift Diff</a><br>
        <a href="/admin/docs/site/index.html" style="color: #4ea1ff; text-decoration: none;">🌐 Static Site</a><br><br>

        <strong>System</strong><br>
        <a href="/admin/logs" style="color: #4ea1ff; text-decoration: none;">📜 Logs</a><br>
        <a href="/admin/system" style="color: #4ea1ff; text-decoration: none;">🖥️ System Panel</a><br>
    </div>
    """
