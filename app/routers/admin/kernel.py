from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import subprocess
import html
import os

router = APIRouter(prefix="/admin/kernel", tags=["Kernel"])


def run_cmd(cmd):
    """Run a shell command safely and return output."""
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
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
def kernel_panel():
    # Kernel version
    uname = run_cmd("uname -a")

    # Kernel command line
    cmdline = read_file("/proc/cmdline")

    # Kernel version string
    version = read_file("/proc/version")

    # Loaded modules
    modules = read_file("/proc/modules")

    # sysctl parameters
    sysctl_all = run_cmd("sysctl -a 2>/dev/null")

    html_page = f"""
    <html>
    <head>
        <title>Kernel Panel</title>
        <meta http-equiv="refresh" content="20">
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
            h2 {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}

        <div style="margin-left: 260px; padding: 20px;">
            <h1>🧬 Kernel Information</h1>
            <p>Auto-refreshing every 20 seconds</p>

            <h2>Kernel Version (uname -a)</h2>
            <pre>{uname}</pre>

            <h2>/proc/version</h2>
            <pre>{version}</pre>

            <h2>Kernel Command Line (/proc/cmdline)</h2>
            <pre>{cmdline}</pre>

            <h2>Loaded Modules (/proc/modules)</h2>
            <pre>{modules}</pre>

            <h2>Kernel Parameters (sysctl -a)</h2>
            <pre>{sysctl_all}</pre>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
