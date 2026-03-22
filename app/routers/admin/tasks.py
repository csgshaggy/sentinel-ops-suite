from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import threading
import asyncio
import html

router = APIRouter(prefix="/admin/tasks", tags=["Tasks"])


def get_async_tasks():
    """Return a list of asyncio tasks if an event loop is running."""
    try:
        loop = asyncio.get_running_loop()
        tasks = asyncio.all_tasks(loop)
        return tasks
    except RuntimeError:
        return []


@router.get("/", response_class=HTMLResponse)
def tasks_panel():
    # Threading info
    threads = threading.enumerate()

    thread_rows = ""
    for t in threads:
        thread_rows += f"""
        <tr>
            <td>{html.escape(t.name)}</td>
            <td>{t.ident}</td>
            <td>{'Alive' if t.is_alive() else 'Dead'}</td>
            <td>{t.daemon}</td>
        </tr>
        """

    # Asyncio tasks
    async_tasks = get_async_tasks()

    async_rows = ""
    for t in async_tasks:
        async_rows += f"""
        <tr>
            <td>{html.escape(str(t))}</td>
            <td>{html.escape(str(t.get_coro()))}</td>
            <td>{html.escape(str(t._state))}</td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Task Manager</title>
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
            <h1>🧵 Task Manager</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <h2>Threading Tasks</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Thread ID</th>
                    <th>Status</th>
                    <th>Daemon</th>
                </tr>
                {thread_rows}
            </table>

            <h2>AsyncIO Tasks</h2>
            <table>
                <tr>
                    <th>Task</th>
                    <th>Coroutine</th>
                    <th>State</th>
                </tr>
                {async_rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
