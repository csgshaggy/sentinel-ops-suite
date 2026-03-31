import html
import os
import subprocess

import psutil
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/limits", tags=["Limits"])


def run_cmd(cmd):
    """Run a shell command safely and return output."""
    try:
        result = subprocess.check_output(
            cmd, shell=True, text=True, stderr=subprocess.STDOUT
        )
        return html.escape(result)
    except Exception as e:
        return f"Error: {html.escape(str(e))}"


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
def limits_panel():
    # ulimit output
    ulimit_all = run_cmd("ulimit -a 2>/dev/null")

    # /proc/self/limits
    proc_limits = read_file("/proc/self/limits")

    # Kernel limits
    file_max = read_file("/proc/sys/fs/file-max")
    pid_max = read_file("/proc/sys/kernel/pid_max")

    # Open file count
    process = psutil.Process(os.getpid())
    open_files = "<br>".join(html.escape(f.path) for f in process.open_files())

    html_page = f"""
    <html>
    <head>
        <title>Resource Limits</title>
        <meta http-equiv="refresh" content="15">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
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
            .metric {{
                background: white;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
            }}
            h2 {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>📏 Resource Limits Overview</h1>
            <p>Auto-refreshing every 15 seconds</p>

            <div class="metric">
                <h2>ulimit -a</h2>
                <pre>{ulimit_all}</pre>
            </div>

            <div class="metric">
                <h2>/proc/self/limits</h2>
                <pre>{proc_limits}</pre>
            </div>

            <div class="metric">
                <h2>Kernel Limits</h2>
                <pre>
fs.file-max: {file_max}
kernel.pid_max: {pid_max}
                </pre>
            </div>

            <div class="metric">
                <h2>Open Files (Current Process)</h2>
                <pre>{open_files}</pre>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
