from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.ui.sidebar import sidebar
import signal
import inspect
import html

router = APIRouter(prefix="/admin/signals", tags=["Signals"])


def get_signal_handlers():
    """Return a list of (signal_name, handler, source) tuples."""
    handlers = []

    for sig in signal.Signals:
        try:
            handler = signal.getsignal(sig)
        except Exception:
            continue

        # Determine handler type
        if handler is None:
            handler_name = "None"
            module = "N/A"
            source = "N/A"
        elif handler == signal.SIG_DFL:
            handler_name = "SIG_DFL (default)"
            module = "N/A"
            source = "Default handler"
        elif handler == signal.SIG_IGN:
            handler_name = "SIG_IGN (ignored)"
            module = "N/A"
            source = "Ignored"
        else:
            handler_name = getattr(handler, "__name__", str(handler))
            module = getattr(handler, "__module__", "Unknown")

            # Try to get source code
            try:
                source = inspect.getsource(handler)
            except Exception:
                source = "Source unavailable"

        handlers.append((sig.name, handler_name, module, source))

    return handlers


@router.get("/", response_class=HTMLResponse)
def signals_panel():
    handlers = get_signal_handlers()

    rows = ""
    for sig_name, handler_name, module, source in handlers:
        rows += f"""
        <tr>
            <td>{html.escape(sig_name)}</td>
            <td>{html.escape(handler_name)}</td>
            <td>{html.escape(module)}</td>
            <td><pre>{html.escape(source)}</pre></td>
        </tr>
        """

    html_page = f"""
    <html>
    <head>
        <title>Signal Inspector</title>
        <meta http-equiv="refresh" content="15">
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
                max-height: 200px;
                overflow-y: auto;
            }}
        </style>
    </head>
    <body>
        {sidebar()}
        <div style="margin-left: 260px; padding: 20px;">
            <h1>🚨 Signal Handler Inspector</h1>
            <p>Auto-refreshing every 15 seconds</p>

            <table>
                <tr>
                    <th>Signal</th>
                    <th>Handler</th>
                    <th>Module</th>
                    <th>Source Code</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(html_page)
