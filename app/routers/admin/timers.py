from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import threading
import asyncio
import inspect
import html
import time

router = APIRouter(prefix="/admin/timers", tags=["Timers"])


def find_threading_timers():
    """Return all active threading.Timer objects."""
    timers = []
    for t in threading.enumerate():
        if isinstance(t, threading.Timer):
            timers.append(t)
    return timers


def find_asyncio_timers():
    """Return asyncio scheduled callbacks if an event loop is running."""
    try:
        loop = asyncio.get_event_loop()
        scheduled = []
        for handle in loop._scheduled:
            when = getattr(handle, "_when", None)
            callback = getattr(handle, "_callback", None)
            scheduled.append((handle, when, callback))
        return scheduled
    except:
        return []


def find_scheduler_timers():
    """Detect APScheduler or custom scheduler timers."""
    timers = []
    for obj in globals().values():
        if hasattr(obj, "next_run_time"):
            timers.append(obj)
    return timers


@router.get("/", response_class=HTMLResponse)
def timers_panel():
    threading_timers = find_threading_timers()
    asyncio_timers = find_asyncio_timers()
    scheduler_timers = find_scheduler_timers()

    # Build HTML rows
    thread_rows = ""
    for t in threading_timers:
        thread_rows += f"""
        <tr>
            <td>{html.escape(t.name)}</td>
            <td>{t.interval}</td>
            <td>{t.is_alive()}</td>
            <td>{t.daemon}</td>
            <td>{t.finished.is_set()}</td>
        </tr>
        """

    asyncio_rows = ""
    for handle, when, callback in asyncio_timers:
        cb_name = getattr(callback, "__name__", str(callback))
        asyncio_rows += f"""
        <tr>
            <td>{html.escape(cb_name)}</td>
            <td>{when}</td>
            <td>{when - time.time():.2f}</td>
        </tr>
        """

    scheduler_rows = ""
    for job in scheduler_timers:
        scheduler_rows += f"""
        <tr>
            <td>{html.escape(str(job))}</td>
            <td>{html.escape(str(getattr(job, 'next_run_time', 'N/A')))}</td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Timer Inspector</title>
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
                vertical-align: top;
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
            <h1>⏱️ Timer Inspector</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <h2>Threading Timers</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Interval</th>
                    <th>Alive</th>
                    <th>Daemon</th>
                    <th>Finished</th>
                </tr>
                {thread_rows}
            </table>

            <h2>AsyncIO Scheduled Callbacks</h2>
            <table>
                <tr>
                    <th>Callback</th>
                    <th>Scheduled Time</th>
                    <th>Seconds Until Run</th>
                </tr>
                {asyncio_rows}
            </table>

            <h2>Scheduler Timers (APScheduler / Custom)</h2>
            <table>
                <tr>
                    <th>Job</th>
                    <th>Next Run Time</th>
                </tr>
                {scheduler_rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
