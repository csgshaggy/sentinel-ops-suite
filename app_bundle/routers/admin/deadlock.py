import gc
import html
import sys
import threading
import traceback

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/threads/deadlock", tags=["Threads Deadlock"])


LOCK_TYPES = (
    threading.Lock,
    threading.RLock,
    threading.Semaphore,
    threading.BoundedSemaphore,
    threading.Condition,
)


def get_lock_objects():
    locks = []
    for obj in gc.get_objects():
        try:
            if isinstance(obj, LOCK_TYPES):
                locks.append(obj)
        except Exception:
            continue
    return locks


def get_thread_stacks():
    frames = sys._current_frames()
    info = []
    for t in threading.enumerate():
        frame = frames.get(t.ident)
        if not frame:
            stack_text = "No stack frame"
        else:
            stack_text = "".join(traceback.format_stack(frame))
        info.append((t, stack_text))
    return info


def classify_stack(stack_text: str):
    lower = stack_text.lower()
    if "acquire" in lower and "lock" in lower:
        return "WAITING_ON_LOCK"
    if "wait" in lower and "condition" in lower:
        return "WAITING_ON_CONDITION"
    if "join" in lower:
        return "WAITING_ON_THREAD"
    return "RUNNING_OR_IDLE"


@router.get("/", response_class=HTMLResponse)
def deadlock_panel():
    locks = get_lock_objects()
    thread_infos = get_thread_stacks()

    # Lock summary
    lock_rows = ""
    for obj in locks:
        locked = getattr(obj, "locked", lambda: "N/A")()
        waiters = getattr(obj, "_waiters", None)
        waiter_count = len(waiters) if waiters is not None else "N/A"
        lock_rows += f"""
        <tr>
            <td>{html.escape(type(obj).__name__)}</td>
            <td>{html.escape(str(locked))}</td>
            <td>{html.escape(str(waiter_count))}</td>
            <td>{html.escape(hex(id(obj)))}</td>
        </tr>
        """

    # Thread summary
    thread_rows = ""
    for t, stack in thread_infos:
        status = classify_stack(stack)
        thread_rows += f"""
        <tr>
            <td>{html.escape(t.name)}</td>
            <td>{t.ident}</td>
            <td>{"Daemon" if t.daemon else "Normal"}</td>
            <td>{html.escape(status)}</td>
            <td><pre>{html.escape(stack)}</pre></td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Deadlock Inspector</title>
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
            pre {{
                background: #000;
                color: #0f0;
                padding: 10px;
                border-radius: 6px;
                white-space: pre-wrap;
                max-height: 250px;
                overflow-y: auto;
                font-size: 12px;
            }}
            h2 {{
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
(
    "<p>Auto-refreshing every 10 seconds. "
    "Look for many threads in WAITING_ON_LOCK / WAITING_ON_CONDITION "
    "with locked locks.</p>"
)

            <h2>Locks</h2>
            <table>
                <tr>
                    <th>Type</th>
                    <th>Locked</th>
                    <th>Waiters (Condition/Semaphore)</th>
                    <th>Object ID</th>
                </tr>
                {lock_rows}
            </table>

            <h2>Threads & Stack States</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Thread ID</th>
                    <th>Kind</th>
                    <th>Heuristic State</th>
                    <th>Stack Trace</th>
                </tr>
                {thread_rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
