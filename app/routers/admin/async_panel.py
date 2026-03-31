import asyncio
import html
import traceback

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/async", tags=["AsyncIO"])


def get_loop_and_tasks():
    """Try to get the current event loop and its tasks safely."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        return None, [], "No running event loop"

    try:
        tasks = asyncio.all_tasks(loop=loop)
        return loop, list(tasks), None
    except Exception as e:
        return loop, [], f"Error getting tasks: {e}"


def describe_task(task: asyncio.Task):
    """Return a dict describing an asyncio.Task."""
    info = {}
    try:
        info["state"] = task._state  # PENDING, RUNNING, FINISHED, etc.
    except Exception:
        info["state"] = "Unknown"

    try:
        coro = task.get_coro()
        info["coro"] = repr(coro)
    except Exception:
        info["coro"] = "Unavailable"

    try:
        stack = task.get_stack(limit=20)
        if stack:
            frames = []
            for frame in stack:
                frames.extend(traceback.format_stack(frame))
            info["stack"] = "".join(frames)
        else:
            info["stack"] = "No stack (task may be done or idle)"
    except Exception:
        info["stack"] = "Stack unavailable"

    try:
        info["done"] = task.done()
        info["cancelled"] = task.cancelled()
    except Exception:
        info["done"] = "Unknown"
        info["cancelled"] = "Unknown"

    return info


@router.get("/", response_class=HTMLResponse)
def async_panel():
    loop, tasks, error = get_loop_and_tasks()

    # Aggregate state counts
    state_counts = {}
    task_rows = ""

    if loop is None:
        loop_info = "No active event loop detected."
    else:
        loop_info = f"Loop: {repr(loop)}"

    if error:
        loop_info += f" | Error: {html.escape(error)}"

    for t in tasks:
        info = describe_task(t)
        state = info.get("state", "Unknown")
        state_counts[state] = state_counts.get(state, 0) + 1

        task_rows += f"""
        <tr>
            <td>{html.escape(str(id(t)))}</td>
            <td>{html.escape(state)}</td>
            <td>{html.escape(str(info.get('done')))}</td>
            <td>{html.escape(str(info.get('cancelled')))}</td>
            <td><pre>{html.escape(info.get('coro', ''))}</pre></td>
            <td><pre>{html.escape(info.get('stack', ''))}</pre></td>
        </tr>
        """

    # State summary
    summary_lines = []
    for state, count in state_counts.items():
        summary_lines.append(f"{state}: {count}")
    summary_text = "\n".join(summary_lines) if summary_lines else "No tasks found."

    html_page = f"""
    <html>
    <head>
        <title>AsyncIO Inspector</title>
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
            .metric {{
                background: white;
                padding: 20px;
                margin: 10px 0;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>🌀 AsyncIO Loop & Task Inspector</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <div class="metric">
                <h2>Loop Info</h2>
                <pre>{html.escape(loop_info)}</pre>
            </div>

            <div class="metric">
                <h2>Task State Summary</h2>
                <pre>{html.escape(summary_text)}</pre>
            </div>

            <div class="metric">
                <h2>Tasks</h2>
                <table>
                    <tr>
                        <th>Task ID</th>
                        <th>State</th>
                        <th>Done</th>
                        <th>Cancelled</th>
                        <th>Coroutine</th>
                        <th>Stack</th>
                    </tr>
                    {task_rows}
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
