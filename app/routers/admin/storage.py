from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import psutil

router = APIRouter(prefix="/admin/storage", tags=["Storage"])


def format_bytes(num):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024


@router.get("/", response_class=HTMLResponse)
def storage_panel():
    partitions = psutil.disk_partitions(all=False)
    io_stats = psutil.disk_io_counters(perdisk=True)

    rows = ""

    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            read_bytes = (
                io_stats.get(part.device, None).read_bytes
                if part.device in io_stats
                else 0
            )
            write_bytes = (
                io_stats.get(part.device, None).write_bytes
                if part.device in io_stats
                else 0
            )

            rows += f"""
            <tr>
                <td>{part.device}</td>
                <td>{part.mountpoint}</td>
                <td>{part.fstype}</td>
                <td>{format_bytes(usage.total)}</td>
                <td>{format_bytes(usage.used)}</td>
                <td>{format_bytes(usage.free)}</td>
                <td>{usage.percent}%</td>
                <td>{format_bytes(read_bytes)}</td>
                <td>{format_bytes(write_bytes)}</td>
            </tr>
            """
        except PermissionError:
            continue

    html_page = f"""
    <html>
    <head>
        <title>Storage Panel</title>
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
            <h1>💾 Storage Panel</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <table>
                <tr>
                    <th>Device</th>
                    <th>Mount Point</th>
                    <th>Type</th>
                    <th>Total</th>
                    <th>Used</th>
                    <th>Free</th>
                    <th>Usage %</th>
                    <th>Read Bytes</th>
                    <th>Write Bytes</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
