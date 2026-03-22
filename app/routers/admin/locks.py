from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import threading
import sys
import gc
import html

router = APIRouter(prefix="/admin/locks", tags=["Locks"])


LOCK_TYPES = (
    threading.Lock,
    threading.RLock,
    threading.Semaphore,
    threading.BoundedSemaphore,
    threading.Condition,
    threading.Event,
)


def get_lock_objects():
    """Scan GC for lock-like objects."""
    locks = []
    for obj in gc.get_objects():
        try:
            if isinstance(obj, LOCK_TYPES):
                locks.append(obj)
        except:
            pass
    return locks


def describe_lock(obj):
    """Return a dict describing a lock-like object."""
    info = {}

    info["type"] = type(obj).__name__

    # Basic lock state
    try:
        if isinstance(obj, threading.Lock) or isinstance(obj, threading.RLock):
            info["locked"] = obj.locked()
        else:
            info["locked"] = "N/A"
    except:
        info["locked"] = "Unknown"

    # RLock owner
    if isinstance(obj, threading.RLock):
        try:
            info["owner"] = obj._owner
        except:
            info["owner"] = "Unknown"

    # Semaphore count
    if isinstance(obj, (threading.Semaphore, threading.BoundedSemaphore)):
        try:
            info["value"] = obj._value
        except:
            info["value"] = "Unknown"

    # Condition waiters
    if isinstance(obj, threading.Condition):
        try:
            info["waiters"] = len(obj._waiters)
        except:
            info["waiters"] = "Unknown"

    # Event state
    if isinstance(obj, threading.Event):
        try:
            info["is_set"] = obj.is_set()
        except:
            info["is_set"] = "Unknown"

    return info


@router.get("/", response_class=HTMLResponse)
def locks_panel():
    locks = get_lock_objects()

    rows = ""
    for obj in locks:
        info = describe_lock(obj)

        rows += f"""
        <tr>
            <td>{html.escape(info['type'])}</td>
            <td>{html.escape(str(info.get('locked', '')))}</td>
            <td>{html.escape(str(info.get('owner', '')))}</td>
            <td>{html.escape(str(info.get('value', '')))}</td>
            <td>{html.escape(str(info.get('waiters', '')))}</td>
            <td>{html.escape(str(info.get('is_set', '')))}</td>
            <td>{html.escape(hex(id(obj)))}</td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Lock Inspector</title>
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
            <h1>🔒 Lock Inspector</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <table>
                <tr>
                    <th>Type</th>
                    <th>Locked</th>
                    <th>Owner (RLock)</th>
                    <th>Value (Semaphore)</th>
                    <th>Waiters (Condition)</th>
                    <th>Event State</th>
                    <th>Object ID</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
