from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin", tags=["Admin Home"])

@router.get("/", response_class=HTMLResponse)
def admin_home():
    html = f"""
    <html>
    <head>
        <title>SSRF Command Console — Admin</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
            }}
            .card {{
                background: white;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            a {{
                text-decoration: none;
                color: #007bff;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>SSRF Command Console — Admin Panel</h1>

            <div class="card"><a href="/admin/docs/dashboard">📘 Documentation Dashboard</a></div>
            <div class="card"><a href="/admin/logs">📜 Log Viewer</a></div>
            <div class="card"><a href="/admin/system">🖥️ System Health</a></div>
            <div class="card"><a href="/admin/processes">⚙️ Process Viewer</a></div>
            <div class="card"><a href="/admin/network">🌐 Network Panel</a></div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html)
