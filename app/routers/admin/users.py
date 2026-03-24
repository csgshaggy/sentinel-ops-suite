from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import pwd
import subprocess
import html

router = APIRouter(prefix="/admin/users", tags=["Users"])


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
def users_panel():
    # System users from /etc/passwd
    users = pwd.getpwall()

    rows = ""
    for u in users:
        rows += f"""
        <tr>
            <td>{html.escape(u.pw_name)}</td>
            <td>{u.pw_uid}</td>
            <td>{u.pw_gid}</td>
            <td>{html.escape(u.pw_dir)}</td>
            <td>{html.escape(u.pw_shell)}</td>
        </tr>
        """

    # Last login info
    last_logins = run_cmd("last -n 20")

    html_page = f"""
    <html>
    <head>
        <title>User Accounts</title>
        <meta http-equiv="refresh" content="15">
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
        </style>
    </head>
    <body>
        {sidebar()}

        <div style="margin-left: 260px; padding: 20px;">
            <h1>👤 User Accounts</h1>
            <p>Auto-refreshing every 15 seconds</p>

            <h2>System Users</h2>
            <table>
                <tr>
                    <th>Username</th>
                    <th>UID</th>
                    <th>GID</th>
                    <th>Home Directory</th>
                    <th>Shell</th>
                </tr>
                {rows}
            </table>

            <h2>Recent Logins</h2>
            <pre>{last_logins}</pre>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
