import html
import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/logs", tags=["Logs"])

LOG_FILE = "app.log"


@router.get("/", response_class=HTMLResponse)
def view_logs():
    if not os.path.exists(LOG_FILE):
        logs_output = "Log file not found."
    else:
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
            logs_output = html.escape(f.read())

    html_page = f"""
    <html>
    <head>
        <title>Log Viewer</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{
                background: #1a1a1a;
                color: #e0e0e0;
                font-family: Consolas, monospace;
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
                max-height: 85vh;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>📜 Log Viewer</h1>
            <pre>{logs_output}</pre>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html_page)
