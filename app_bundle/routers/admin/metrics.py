import datetime

import psutil
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/metrics", tags=["Metrics"])


def format_bytes(num):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024


@router.get("/", response_class=HTMLResponse)
def metrics_panel():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.5)
    per_core = psutil.cpu_percent(interval=0.5, percpu=True)

    # Memory
    mem = psutil.virtual_memory()

    # Disk I/O
    disk_io = psutil.disk_io_counters()

    # Network I/O
    net_io = psutil.net_io_counters()

    # Uptime
    boot = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot

    # Build per-core rows
    core_rows = ""
    for idx, val in enumerate(per_core):
        core_rows += f"<tr><td>Core {idx}</td><td>{val}%</td></tr>"

    html_page = f"""
    <html>
    <head>
        <title>Metrics Dashboard</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
            }}
            .metric {{
                background: white;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
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
        </style>
    </head>
    <body>
        {sidebar()}

        <div style="margin-left: 260px; padding: 20px;">
            <h1>📊 Metrics Dashboard</h1>
            <p>Auto-refreshing every 5 seconds</p>

            <div class="metric">
                <h2>CPU Usage</h2>
                <p>Total CPU: {cpu_percent}%</p>
                <table>
                    <tr><th>Core</th><th>Usage</th></tr>
                    {core_rows}
                </table>
            </div>

            <div class="metric">
                <h2>Memory Usage</h2>
                <p>{mem.percent}% ({format_bytes(mem.used)} / {format_bytes(mem.total)})</p>
            </div>

            <div class="metric">
                <h2>Disk I/O</h2>
                <p>Read: {format_bytes(disk_io.read_bytes)}</p>
                <p>Write: {format_bytes(disk_io.write_bytes)}</p>
            </div>

            <div class="metric">
                <h2>Network I/O</h2>
                <p>Sent: {format_bytes(net_io.bytes_sent)}</p>
                <p>Received: {format_bytes(net_io.bytes_recv)}</p>
            </div>

            <div class="metric">
                <h2>System Uptime</h2>
                <p>{str(uptime).split(".")[0]}</p>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
