from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import subprocess
import html

router = APIRouter(prefix="/admin/security", tags=["Security"])


def run_cmd(cmd):
    """Run a shell command safely and return output."""
    try:
        result = subprocess.check_output(
            cmd, shell=True, text=True, stderr=subprocess.STDOUT
        )
        return html.escape(result)
    except Exception as e:
        return f"Error: {html.escape(str(e))}"


@router.get("/", response_class=HTMLResponse)
def security_panel():
    # Linux authentication logs
    last_logins = run_cmd("last -n 20")
    failed_logins = run_cmd("lastb -n 20 2>/dev/null")
    who_output = run_cmd("who")

    html_page = f"""
    <html>
    <head>
        <title>Security Panel</title>
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
            <h1>🔐 Security Panel</h1>
            <p>Authentication and session activity overview</p>

            <h2>Active Sessions (who)</h2>
            <pre>{who_output}</pre>

            <h2>Recent Logins (last)</h2>
            <pre>{last_logins}</pre>

            <h2>Failed Login Attempts (lastb)</h2>
            <pre>{failed_logins}</pre>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
