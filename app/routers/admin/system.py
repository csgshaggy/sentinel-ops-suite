from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import psutil
import datetime
import platform

router = APIRouter(prefix="/admin/system", tags=["System"])

def format_bytes(num):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024

@router.get("/", response_class=HTMLResponse)
def system_dashboard():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    boot = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot

    html_page = f"""
    <html>
    <head>
        <title>System Dashboard</title>
        <style>
            body {{
                font-family: Arial;
                background: #f4f4f4;
                margin: 0;
            }}
            .metric {{
                background: white;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>🖥️ System Dashboard</h1>

            <div class="metric">CPU Usage: {cpu}%</div>
            <div class="metric">Memory: {mem.percent}% ({format_bytes(mem.used)} / {format_bytes(mem.total)})</div>
            <div class="metric">Disk: {disk.percent}% ({format_bytes(disk.used)} / {format_bytes(disk.total)})</div>
            <div class="metric">Uptime: {str(uptime).split('.')[0]}</div>
            <div class="metric">OS: {platform.system()} {platform.release()}</div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html_page)
