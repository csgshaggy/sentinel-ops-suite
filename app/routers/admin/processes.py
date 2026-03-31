import psutil
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/processes", tags=["Processes"])


@router.get("/", response_class=HTMLResponse)
def list_processes():
    processes = []

    for proc in psutil.process_iter(
        attrs=["pid", "name", "status", "cpu_percent", "memory_info"]
    ):
        try:
            info = proc.info
            processes.append(
                {
                    "pid": info["pid"],
                    "name": info.get("name", "N/A"),
                    "status": info.get("status", "N/A"),
                    "cpu": info.get("cpu_percent", 0.0),
                    "memory": info["memory_info"].rss if info.get("memory_info") else 0,
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort by CPU usage descending
    processes = sorted(processes, key=lambda p: p["cpu"], reverse=True)

    # Build HTML table rows
    rows = ""
    for p in processes:
        rows += f"""
        <tr>
            <td>{p["pid"]}</td>
            <td>{p["name"]}</td>
            <td>{p["status"]}</td>
            <td>{p["cpu"]}%</td>
            <td>{p["memory"] / (1024 * 1024):.2f} MB</td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Process Viewer</title>
        <meta http-equiv="refresh" content="5"> <!-- auto-refresh -->
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
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            th, td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}
            th {{
                background: #333;
                color: white;
            }}
            tr:hover {{
                background: #f1f1f1;
            }}
            h1 {{
                color: #333;
            }}
        </style>
    </head>
    <body>
        {sidebar()}

        <div style="margin-left: 260px; padding: 20px;">
            <h1>⚙️ Process Viewer</h1>
            <p>Auto-refreshing every 5 seconds</p>

            <table>
                <tr>
                    <th>PID</th>
                    <th>Name</th>
                    <th>Status</th>
                    <th>CPU %</th>
                    <th>Memory</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
