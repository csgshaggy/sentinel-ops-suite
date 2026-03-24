from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import subprocess
import html
import os

router = APIRouter(prefix="/admin/hardware", tags=["Hardware"])


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
def hardware_panel():
    # CPU info
    cpuinfo = read_file("/proc/cpuinfo")

    # Memory info
    meminfo = read_file("/proc/meminfo")

    # Block devices
    block_devices = run_cmd("lsblk -o NAME,SIZE,TYPE,MOUNTPOINT 2>/dev/null")

    # PCI devices
    pci_devices = run_cmd("lspci 2>/dev/null")

    # USB devices
    usb_devices = run_cmd("lsusb 2>/dev/null")

    # Sensors (if available)
    sensors = run_cmd("sensors 2>/dev/null")

    html_page = f"""
    <html>
    <head>
        <title>Hardware Panel</title>
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
            <h1>🖥️ Hardware Overview</h1>
            <p>Auto-refreshing every 20 seconds</p>

            <h2>CPU Information (/proc/cpuinfo)</h2>
            <pre>{cpuinfo}</pre>

            <h2>Memory Information (/proc/meminfo)</h2>
            <pre>{meminfo}</pre>

            <h2>Block Devices (lsblk)</h2>
            <pre>{block_devices}</pre>

            <h2>PCI Devices (lspci)</h2>
            <pre>{pci_devices}</pre>

            <h2>USB Devices (lsusb)</h2>
            <pre>{usb_devices}</pre>

            <h2>Hardware Sensors (sensors)</h2>
            <pre>{sensors}</pre>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
