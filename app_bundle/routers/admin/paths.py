import html
import os
import sys
from pathlib import Path

import psutil
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/paths", tags=["Paths"])


def tree(path, depth=2):
    """Return a small directory tree snapshot."""
    try:
        base = Path(path)
        lines = []

        for root, dirs, files in os.walk(base):
            level = Path(root).relative_to(base).parts
            if len(level) > depth:
                continue

            indent = " " * (len(level) * 4)
            lines.append(f"{indent}{os.path.basename(root)}/")

            for f in files:
                lines.append(f"{indent}    {f}")

        return "<br>".join(html.escape(line) for line in lines)
    except Exception as e:
        return f"Error: {html.escape(str(e))}"


@router.get("/", response_class=HTMLResponse)
def paths_panel():
    # Core paths
    cwd = os.getcwd()
    home = str(Path.home())
    python_exec = sys.executable
    project_root = str(Path(__file__).resolve().parents[3])

    # Python path
    python_path = "<br>".join(html.escape(p) for p in sys.path)

    # Open files
    process = psutil.Process(os.getpid())
    open_files = "<br>".join(html.escape(f.path) for f in process.open_files())

    # Directory trees
    tree_project = tree(project_root, depth=2)
    tree_cwd = tree(cwd, depth=2)

    html_page = f"""
    <html>
    <head>
        <title>Paths Inspector</title>
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
            <h1>📁 Path & Filesystem Inspector</h1>
            <p>Auto-refreshing every 15 seconds</p>

            <div class="metric">
                <h2>Core Paths</h2>
                <pre>
Project Root: {project_root}
Working Directory: {cwd}
Home Directory: {home}
Python Executable: {python_exec}
                </pre>
            </div>

            <div class="metric">
                <h2>Python Path (sys.path)</h2>
                <pre>{python_path}</pre>
            </div>

            <div class="metric">
                <h2>Open Files (Current Process)</h2>
                <pre>{open_files}</pre>
            </div>

            <div class="metric">
                <h2>Directory Tree: Project Root</h2>
                <pre>{tree_project}</pre>
            </div>

            <div class="metric">
                <h2>Directory Tree: Working Directory</h2>
                <pre>{tree_cwd}</pre>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
