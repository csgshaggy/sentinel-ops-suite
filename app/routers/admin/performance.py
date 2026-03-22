from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import psutil
import html
import os

router = APIRouter(prefix="/admin/performance", tags=["Performance"])


def read_file(path):
    """Safely read a file if it exists."""
    if os.path.exists(path):
        try:
            with open(path, "r", errors="ignore") as f:
                return html.escape(f.read())
        except Exception as e:
            return f"Error reading {path}: {html.escape(str(e))}"
    return f"{path} not found"


@router.get("/", response_class=HTMLResponse)
def performance_panel():
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=0.5)
    load1, load5, load15 = os.getloadavg()

    # Memory
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    # I/O wait (from psutil.cpu_times)
    cpu_times = psutil.cpu_times()
    iowait = getattr(cpu_times, "iowait", 0)

    # Context switches & interrupts
    proc_stat = read_file("/proc/stat")

    # Uptime
    uptime = read_file("/proc/uptime")

    # Loadavg
    loadavg = read_file("/proc/loadavg")

    html_page = f"""
    <html>
    <head>
        <title>Performance Panel</title>
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
            pre {{
                background: #000;
                color: #0f0;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                white-space: pre-wrap;
                font-size: 14px;
                max-height: 40vh;
            }}
            h2 {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}

        <div style="margin-left: 260px; padding: 20px;">
            <h1>⚡ Performance Diagnostics</h1>
            <p>Auto-refreshing every 5 seconds</p>

            <div class="metric">
                <h2>CPU Pressure</h2>
                <p>CPU Usage: {cpu_percent}%</p>
                <p>Load Average: {load1}, {load5}, {load15}</p>
                <p>I/O Wait: {iowait}</p>
            </div>

            <div class="metric">
                <h2>Memory Pressure</h2>
                <p>Used: {mem.percent}% ({mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB)</p>
                <p>Swap Used: {swap.percent}%</p>
            </div>

            <div class="metric">
                <h2>Load Average (/proc/loadavg)</h2>
                <pre>{loadavg}</pre>
            </div>

            <div class="metric">
                <h2>Context Switches & Interrupts (/proc/stat)</h2>
                <pre>{proc_stat}</pre>
            </div>

            <div class="metric">
                <h2>System Uptime (/proc/uptime)</h2>
                <pre>{uptime}</pre>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
