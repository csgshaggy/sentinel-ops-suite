from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import subprocess
import html

router = APIRouter(prefix="/admin/events", tags=["Events"])


def run_cmd(cmd):
    """Run a shell command safely and return output."""
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        return html.escape(result)
    except Exception as e:
        return f"Error: {html.escape(str(e))}"


@router.get("/", response_class=HTMLResponse)
def events_panel():
    # Kernel messages
    dmesg_output = run_cmd("dmesg | tail -n 200")

    # System journal (if available)
    journal_output = run_cmd("journalctl -n 200 2>/dev/null")

    # Errors only
    journal_errors = run_cmd("journalctl -p err -n 100 2>/dev/null")

    html_page = f"""
    <html>
    <head>
        <title>System Events</title>
        <meta http-equiv="refresh" content="10">
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
            <h1>📡 System Events</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <h2>Kernel Messages (dmesg)</h2>
            <pre>{dmesg_output}</pre>

            <h2>System Journal (journalctl)</h2>
            <pre>{journal_output}</pre>

            <h2>Error Events (journalctl -p err)</h2>
            <pre>{journal_errors}</pre>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
