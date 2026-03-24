from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import subprocess
import html
import os

router = APIRouter(prefix="/admin/boot", tags=["Boot"])


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
def boot_panel():
    # Current boot logs
    current_boot = run_cmd("journalctl -b -n 200 2>/dev/null")

    # Previous boot logs
    previous_boot = run_cmd("journalctl -b -1 -n 200 2>/dev/null")

    # Failed boot units
    failed_units = run_cmd("systemctl --failed 2>/dev/null")

    # Bootloader config (GRUB)
    grub_cfg = read_file("/boot/grub/grub.cfg")
    if "not found" in grub_cfg:
        grub_cfg = read_file("/boot/grub2/grub.cfg")

    # Kernel boot messages
    dmesg_head = run_cmd("dmesg | head -n 50")

    html_page = f"""
    <html>
    <head>
        <title>Boot Panel</title>
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
            <h1>🚀 Boot Diagnostics</h1>
            <p>Auto-refreshing every 20 seconds</p>

            <h2>Current Boot Logs (journalctl -b)</h2>
            <pre>{current_boot}</pre>

            <h2>Previous Boot Logs (journalctl -b -1)</h2>
            <pre>{previous_boot}</pre>

            <h2>Failed Boot Units (systemctl --failed)</h2>
            <pre>{failed_units}</pre>

            <h2>Bootloader Configuration (GRUB)</h2>
            <pre>{grub_cfg}</pre>

            <h2>Kernel Boot Messages (dmesg)</h2>
            <pre>{dmesg_head}</pre>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
