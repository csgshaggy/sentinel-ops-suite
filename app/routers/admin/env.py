from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import os
import pwd
import grp
import html

router = APIRouter(prefix="/admin/env", tags=["Environment"])


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
def env_panel():
    # Environment variables
    env_vars = "<br>".join(f"{html.escape(k)}={html.escape(v)}" for k, v in os.environ.items())

    # .env file
    dotenv = read_file(".env")

    # Working directory
    cwd = os.getcwd()

    # Python path
    python_path = "<br>".join(html.escape(p) for p in os.sys.path)

    # User info
    uid = os.getuid()
    gid = os.getgid()
    user_info = pwd.getpwuid(uid)
    group_info = grp.getgrgid(gid)

    html_page = f"""
    <html>
    <head>
        <title>Environment Panel</title>
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
            <h1>🌱 Environment Overview</h1>
            <p>Auto-refreshing every 15 seconds</p>

            <div class="metric">
                <h2>Environment Variables</h2>
                <pre>{env_vars}</pre>
            </div>

            <div class="metric">
                <h2>.env File</h2>
                <pre>{dotenv}</pre>
            </div>

            <div class="metric">
                <h2>Working Directory</h2>
                <pre>{cwd}</pre>
            </div>

            <div class="metric">
                <h2>Python Path (sys.path)</h2>
                <pre>{python_path}</pre>
            </div>

            <div class="metric">
                <h2>User & Group Info</h2>
                <pre>
User: {user_info.pw_name}
UID: {uid}
GID: {gid}
Group: {group_info.gr_name}
Home: {user_info.pw_dir}
Shell: {user_info.pw_shell}
                </pre>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
