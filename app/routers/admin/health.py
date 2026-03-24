from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import psutil
import subprocess
import html

router = APIRouter(prefix="/admin/health", tags=["Health"])


def run_cmd(cmd):
    """Run a shell command safely and return output."""
    try:
        result = subprocess.check_output(
            cmd, shell=True, text=True, stderr=subprocess.STDOUT
        )
        return html.escape(result)
    except Exception as e:
        return f"Error: {html.escape(str(e))}"


def compute_health_score(cpu, mem, disk, swap, failed_services):
    """Compute a simple health score from 0–100."""
    score = 100

    # CPU pressure
    if cpu > 90:
        score -= 25
    elif cpu > 75:
        score -= 10

    # Memory pressure
    if mem > 90:
        score -= 25
    elif mem > 75:
        score -= 10

    # Disk pressure
    if disk > 90:
        score -= 20
    elif disk > 75:
        score -= 10

    # Swap usage
    if swap > 50:
        score -= 15

    # Failed services
    if "failed" in failed_services.lower():
        score -= 20

    return max(score, 0)


@router.get("/", response_class=HTMLResponse)
def health_panel():
    # CPU
    cpu = psutil.cpu_percent(interval=0.5)

    # Memory
    mem = psutil.virtual_memory().percent

    # Disk
    disk = psutil.disk_usage("/").percent

    # Swap
    swap = psutil.swap_memory().percent

    # Failed services
    failed_services = run_cmd("systemctl --failed 2>/dev/null")

    # Kernel warnings
    kernel_warnings = run_cmd("dmesg | grep -i 'warn\\|error\\|fail' | tail -n 20")

    # Compute health score
    score = compute_health_score(cpu, mem, disk, swap, failed_services)

    # Color coding
    color = "#0f0" if score >= 80 else "#ff0" if score >= 50 else "#f00"

    html_page = f"""
    <html>
    <head>
        <title>System Health</title>
        <meta http-equiv="refresh" content="10">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
            }}
            .metric {{
                background: white;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
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
            .score {{
                font-size: 48px;
                font-weight: bold;
                color: {color};
            }}
            h2 {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>❤️ System Health Overview</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <div class="metric">
                <h2>Health Score</h2>
                <div class="score">{score}</div>
            </div>

            <div class="metric">
                <h2>Resource Pressure</h2>
                <p>CPU Usage: {cpu}%</p>
                <p>Memory Usage: {mem}%</p>
                <p>Disk Usage (/): {disk}%</p>
                <p>Swap Usage: {swap}%</p>
            </div>

            <div class="metric">
                <h2>Failed Services</h2>
                <pre>{failed_services}</pre>
            </div>

            <div class="metric">
                <h2>Kernel Warnings</h2>
                <pre>{kernel_warnings}</pre>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
