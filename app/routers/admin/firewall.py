from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import subprocess
import html

router = APIRouter(prefix="/admin/firewall", tags=["Firewall"])


def run_cmd(cmd):
    """Run a shell command safely and return output."""
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        return html.escape(result)
    except Exception as e:
        return f"Error: {html.escape(str(e))}"


@router.get("/", response_class=HTMLResponse)
def firewall_panel():
    # Try UFW first
    ufw_status = run_cmd("ufw status verbose 2>/dev/null")

    # Try firewall-cmd (RHEL/CentOS)
    firewall_cmd_status = run_cmd("firewall-cmd --list-all 2>/dev/null")

    # Fallback: iptables
    iptables_rules = run_cmd("iptables -L -n -v 2>/dev/null")

    html_page = f"""
    <html>
    <head>
        <title>Firewall Panel</title>
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
            h2 {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}

        <div style="margin-left: 260px; padding: 20px;">
            <h1>🛡️ Firewall Panel</h1>
            <p>Auto-refreshing every 15 seconds</p>

            <h2>UFW Status</h2>
            <pre>{ufw_status}</pre>

            <h2>firewall-cmd (RHEL/CentOS)</h2>
            <pre>{firewall_cmd_status}</pre>

            <h2>iptables Rules</h2>
            <pre>{iptables_rules}</pre>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
