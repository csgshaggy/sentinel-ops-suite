import html
import threading

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/scheduler", tags=["Scheduler"])


def detect_scheduler():
    """Try to detect APScheduler if installed and running."""
    try:
        # Try to find any running scheduler instance
        schedulers = []

        # Check common global scheduler names
        for name in ["scheduler", "sched", "apscheduler", "job_scheduler"]:
            if name in globals():
                schedulers.append(globals()[name])

        # Fallback: try to detect running schedulers by scanning threads
        for t in threading.enumerate():
            if "APScheduler" in t.name:
                schedulers.append(t)

        return schedulers

    except Exception:
        return []


def get_jobs():
    """Return APScheduler jobs if available."""
    try:
        jobs = []

        # Try to find a scheduler instance
        for obj in globals().values():
            if hasattr(obj, "get_jobs"):
                try:
                    jobs.extend(obj.get_jobs())
                except Exception:
                    pass

        return jobs

    except Exception:
        return []


@router.get("/", response_class=HTMLResponse)
def scheduler_panel():
    schedulers = detect_scheduler()
    jobs = get_jobs()

    # Build scheduler rows
    scheduler_rows = ""
    if schedulers:
        for s in schedulers:
            scheduler_rows += f"""
            <tr>
                <td>{html.escape(str(s))}</td>
                <td>{html.escape(getattr(s, "state", "Unknown"))}</td>
                <td>{html.escape(str(getattr(s, "running", "Unknown")))}</td>
            </tr>
            """
    else:
        scheduler_rows = (
            "<tr><td colspan='3'>No APScheduler instance detected</td></tr>"
        )

    # Build job rows
    job_rows = ""
    if jobs:
        for j in jobs:
            job_rows += f"""
            <tr>
                <td>{html.escape(j.id)}</td>
                <td>{html.escape(str(j.trigger))}</td>
                <td>{html.escape(str(j.next_run_time))}</td>
            </tr>
            """
    else:
        job_rows = "<tr><td colspan='3'>No scheduled jobs found</td></tr>"

    html_page = f"""
    <html>
    <head>
        <title>Scheduler Panel</title>
        <meta http-equiv="refresh" content="10">
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
            h2 {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}

        <div style="margin-left: 260px; padding: 20px;">
            <h1>⏱️ Scheduler Panel</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <h2>Detected Schedulers</h2>
            <table>
                <tr>
                    <th>Scheduler</th>
                    <th>State</th>
                    <th>Running</th>
                </tr>
                {scheduler_rows}
            </table>

            <h2>Scheduled Jobs</h2>
            <table>
                <tr>
                    <th>Job ID</th>
                    <th>Trigger</th>
                    <th>Next Run</th>
                </tr>
                {job_rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
