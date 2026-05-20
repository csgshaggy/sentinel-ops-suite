import html
import sys
import threading

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.ui.sidebar import sidebar

router = APIRouter(prefix="/admin/threads", tags=["Threads"])


def get_thread_stacks():
    """Return stack traces for all threads."""
    frames = sys._current_frames()
    output = ""

    for thread in threading.enumerate():
        ident = thread.ident
        frame = frames.get(ident)

        if frame:
            stack_lines = []
            while frame:
                code = frame.f_code
                stack_lines.append(
                    f"File: {code.co_filename}, Line: {frame.f_lineno}, Function: {code.co_name}"
                )
                frame = frame.f_back

            stack_text = "<br>".join(html.escape(line) for line in stack_lines)
        else:
            stack_text = "No stack frame available"

        output += f"""
        <tr>
            <td>{html.escape(thread.name)}</td>
            <td>{ident}</td>
            <td>{"Alive" if thread.is_alive() else "Dead"}</td>
            <td>{thread.daemon}</td>
            <td>{stack_text}</td>
        </tr>
        """

    return output


@router.get("/", response_class=HTMLResponse)
def threads_panel():
    threads = threading.enumerate()
    thread_count = len(threads)

    thread_rows = get_thread_stacks()

    html_page = f"""
    <html>
    <head>
        <title>Thread Inspector</title>
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
            .count-box {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                font-size: 20px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>🧵 Thread Inspector</h1>
            <p>Auto-refreshing every 10 seconds</p>

            <div class="count-box">
                Active Threads: {thread_count}
            </div>

            <table>
                <tr>
                    <th>Name</th>
                    <th>Thread ID</th>
                    <th>Status</th>
                    <th>Daemon</th>
                    <th>Stack Trace</th>
                </tr>
                {thread_rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
