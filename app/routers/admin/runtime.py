from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import platform
import sys
import os
import psutil
import html
import inspect

router = APIRouter(prefix="/admin/runtime", tags=["Runtime"])


def format_bytes(num):
    for unit in ["B", "KB", "MB", "GB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024


@router.get("/", response_class=HTMLResponse)
def runtime_panel():
    # Python version
    python_version = platform.python_version()
    python_build = platform.python_build()
    python_compiler = platform.python_compiler()

    # Loaded modules
    loaded_modules = "<br>".join(sorted(html.escape(m) for m in sys.modules.keys()))

    # Environment variables
    env_vars = "<br>".join(f"{html.escape(k)}={html.escape(v)}" for k, v in os.environ.items())

    # Python path
    python_path = "<br>".join(html.escape(p) for p in sys.path)

    # Working directory
    cwd = os.getcwd()

    # Process memory usage
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    rss = format_bytes(mem_info.rss)
    vms = format_bytes(mem_info.vms)

    html_page = f"""
    <html>
    <head>
        <title>Runtime Panel</title>
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
            <h1>🐍 Python Runtime Diagnostics</h1>
            <p>Auto-refreshing every 15 seconds</p>

            <div class="metric">
                <h2>Interpreter Info</h2>
                <p>Python Version: {python_version}</p>
                <p>Build: {python_build}</p>
                <p>Compiler: {python_compiler}</p>
                <p>Working Directory: {cwd}</p>
            </div>

            <div class="metric">
                <h2>Process Memory Usage</h2>
                <p>RSS: {rss}</p>
                <p>VMS: {vms}</p>
            </div>

            <div class="metric">
                <h2>Python Path (sys.path)</h2>
                <pre>{python_path}</pre>
            </div>

            <div class="metric">
                <h2>Environment Variables</h2>
                <pre>{env_vars}</pre>
            </div>

            <div class="metric">
                <h2>Loaded Modules</h2>
                <pre>{loaded_modules}</pre>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
