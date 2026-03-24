from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import subprocess
import html

router = APIRouter(prefix="/admin/audit", tags=["Audit"])


def run_cmd(cmd):
    """Run a shell command safely and return output or error."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return f"Command failed: {html.escape(result.stderr.strip())}"
    except Exception as e:
        return f"Error: {html.escape(str(e))}"


def get_auth_log():
    """Return authentication-related events from /var/log/auth.log or journalctl."""
    # Debian/Ubuntu
    out = run_cmd(
        "grep -E 'Failed|Accepted|sudo|authentication' /var/log/auth.log 2>/dev/null | tail -n 200"
    )
    if "No such file" not in out and out.strip():
        return out

    # RHEL/Fedora/CentOS
    out = run_cmd("journalctl -u ssh --no-pager -n 200")
    if out.strip():
        return out

    return "No authentication logs available."


def get_auditd_log():
    """Return auditd events if auditd is installed."""
    out = run_cmd(
        "ausearch -m USER_LOGIN,USER_AUTH,USER_CMD,EXECVE -ts recent 2>/dev/null | tail -n 200"
    )
    if "ausearch" not in out and out.strip():
        return out

    return "auditd not installed or no audit events available."


@router.get("/", response_class=HTMLResponse)
def audit_panel():
    auth_log = get_auth_log()
    auditd_log = get_auditd_log()

    html_page = f"""
    <html>
    <head>
        <title>Audit Logs</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #121212;
                color: #e0e0e0;
                margin: 0;
            }}
            pre {{
                background: #000;
                color: #00ff90;
                padding: 12px;
                border-radius: 6px;
                white-space: pre-wrap;
            }}
            h1, h2 {{
                color: white;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left:260px;padding:20px;">
            <h1>🔍 Audit & Security Events</h1>
            <p>Authentication attempts, sudo usage, privilege escalations, and auditd events.</p>

            <h2>Authentication Log</h2>
            <pre>{html.escape(auth_log)}</pre>

            <h2>Auditd Events</h2>
            <pre>{html.escape(auditd_log)}</pre>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
