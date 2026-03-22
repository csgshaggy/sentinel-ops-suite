from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import psutil

router = APIRouter(prefix="/admin/services", tags=["Services"])


@router.get("/", response_class=HTMLResponse)
def services_panel():
    services = []

    # psutil.win_service_iter() works on Windows
    # psutil.process_iter() fallback for Linux/macOS
    try:
        win_services = list(psutil.win_service_iter())
        for svc in win_services:
            try:
                info = svc.as_dict()
                services.append({
                    "name": info.get("name", "N/A"),
                    "display_name": info.get("display_name", "N/A"),
                    "status": info.get("status", "unknown"),
                    "start_type": info.get("start_type", "N/A"),
                })
            except Exception:
                continue
    except Exception:
        # Linux/macOS fallback: treat processes as "services"
        for proc in psutil.process_iter(attrs=["pid", "name", "status"]):
            try:
                info = proc.info
                services.append({
                    "name": info.get("name", "N/A"),
                    "display_name": info.get("name", "N/A"),
                    "status": info.get("status", "unknown"),
                    "start_type": "process",
                })
            except Exception:
                continue

    # Sort alphabetically
    services = sorted(services, key=lambda s: s["name"].lower())

    rows = ""
    for svc in services:
        rows += f"""
        <tr>
            <td>{svc['name']}</td>
            <td>{svc['display_name']}</td>
            <td>{svc['status']}</td>
            <td>{svc['start_type']}</td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Service Manager</title>
        <meta http-equiv="refresh" content="10">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}
            th {{
                background: #333;
                color: white;
            }}
            th, td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            tr:hover {{
                background: #f1f1f1;
            }}
        </style>
    </head>
    <body>
        {sidebar()}

        <div style="margin-left: 260px; padding: 20px;">
            <h1>🛠️ Service Manager</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <table>
                <tr>
                    <th>Name</th>
                    <th>Display Name</th>
                    <th>Status</th>
                    <th>Start Type</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
